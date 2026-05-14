import pytest
from app import app as flask_app
from database.db import init_db, get_db

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': 'file:memdb1?mode=memory&cache=shared',  # shared in-memory DB for tests
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })
    with flask_app.app_context():
        init_db()
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in."""
    # Register a user first
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    # Log in
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    return client

class TestAddExpense:
    def test_add_expense_accessible_for_logged_in_user(self, auth_client):
        """User can navigate to /expenses/add while logged in."""
        response = auth_client.get('/expenses/add')
        assert response.status_code == 200
        assert b'Add Expense' in response.data or b'amount' in response.data.lower()

    def test_add_expense_redirects_guest_user(self, client):
        """Guest users are redirected to the login page when accessing /expenses/add."""
        response = client.get('/expenses/add', follow_redirects=False)
        assert response.status_code == 302
        assert response.location == '/login'

    def test_add_expense_success(self, auth_client, app):
        """Submitted expenses are correctly inserted into the DB and user is redirected to profile."""
        expense_data = {
            'amount': '150.50',
            'category': 'Food',
            'date': '2026-05-14',
            'description': 'Lunch with team'
        }

        response = auth_client.post('/expenses/add', data=expense_data, follow_redirects=False)

        # Verify redirect to profile
        assert response.status_code == 302
        assert response.location == '/profile'

        # Verify DB side effect
        with app.app_context():
            db = get_db()
            row = db.execute(
                "SELECT * FROM expenses WHERE amount = ? AND category = ? AND date = ?",
                (150.50, 'Food', '2026-05-14')
            ).fetchone()
            db.close()

            assert row is not None, "Expense should be saved in the database"
            assert row['description'] == 'Lunch with team'
            # Ensure user_id is present (not null)
            assert row['user_id'] is not None

    @pytest.mark.parametrize("missing_field", ['amount', 'category', 'date'])
    def test_add_expense_missing_required_fields(self, auth_client, missing_field):
        """Form displays errors for missing required fields."""
        expense_data = {
            'amount': '150.50',
            'category': 'Food',
            'date': '2026-05-14',
            'description': 'Valid'
        }
        del expense_data[missing_field]

        response = auth_client.post('/expenses/add', data=expense_data)
        assert response.status_code == 200
        assert b'required' in response.data.lower(), f"Expected error for missing {missing_field}"

    def test_add_expense_invalid_amount_negative(self, auth_client):
        """Form displays errors for negative amount."""
        expense_data = {
            'amount': '-10.00',
            'category': 'Food',
            'date': '2026-05-14',
            'description': 'Negative'
        }
        response = auth_client.post('/expenses/add', data=expense_data)
        assert response.status_code == 200
        assert b'positive amount' in response.data.lower()

    def test_add_expense_invalid_amount_non_numeric(self, auth_client):
        """Form displays errors for non-numeric amount."""
        expense_data = {
            'amount': 'abc',
            'category': 'Food',
            'date': '2026-05-14',
            'description': 'Non-numeric'
        }
        response = auth_client.post('/expenses/add', data=expense_data)
        assert response.status_code == 200
        assert b'valid positive amount' in response.data.lower()

    def test_add_expense_invalid_date_format(self, auth_client):
        """Form displays errors for invalid date format."""
        expense_data = {
            'amount': '100',
            'category': 'Food',
            'date': '14-05-2026', # Wrong format (DD-MM-YYYY instead of YYYY-MM-DD)
            'description': 'Wrong Date'
        }
        response = auth_client.post('/expenses/add', data=expense_data)
        assert response.status_code == 200
        assert b'valid date' in response.data.lower()

    def test_add_expense_invalid_category(self, auth_client):
        """Form displays errors for invalid category."""
        expense_data = {
            'amount': '100',
             'category': 'Luxury Cruise', # Not in the predefined list
            'date': '2026-05-14',
            'description': 'Invalid Category'
        }
        response = auth_client.post('/expenses/add', data=expense_data)
        assert response.status_code == 200
        assert b'Invalid category' in response.data
