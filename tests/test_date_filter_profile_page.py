# Adjust sys.path to include the project root
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))





import pytest
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from app import app as flask_app
import database.db
import database.db
import database.db
from database.db import init_db, get_db



@pytest.fixture
def app():
    db_uri = 'file:memdb2?mode=memory&cache=shared'
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_uri,
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })
    import database.db
    database.db.DATABASE = db_uri
    # Override the database module's DATABASE variable to use in-memory database
    import database.db
    database.db.DATABASE = ':memory:'
    with flask_app.app_context():
        init_db()
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in."""
    # Register a test user
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!'
    }, follow_redirects=True)
    # Simulate login by setting the session
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    return client
def insert_expense(db, user_id, amount, category, expense_date, description=''):
    """Helper to insert an expense directly into the DB."""
    db.execute(
        '''INSERT INTO expenses (user_id, amount, category, date, description)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, amount, category, expense_date, description)
    )
    db.commit()

def get_profile(client, params=None):
    """Helper to GET /profile with optional query params."""
    return client.get('/profile', query_string=params or {})

def test_profile_requires_login(client):
    """Unauthenticated access to /profile redirects to login."""
    response = client.get('/profile', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.location

def test_profile_no_expenses_shows_zero_state(auth_client):
    """User with no expenses sees zero totals and empty lists."""
    response = auth_client.get('/profile')
    assert response.status_code == 200
    assert '₹0.00' in response.data.decode('utf-8')
    assert b'0 transactions' in response.data

def test_profile_unfiltered_shows_all_expenses(auth_client):
    """Visiting /profile with no query params returns all user's expenses."""
    today = date.today()
    # Insert three expenses on different dates
    with flask_app.app_context():
        db = get_db()
        user_id = 1  # Because auth_client creates user with id=1 (first after init)
        insert_expense(db, user_id, 10.0, 'Food', today.isoformat(), 'Today')
        insert_expense(db, user_id, 20.0, 'Transport', (today - timedelta(days=5)).isoformat(), '5 days ago')
        insert_expense(db, user_id, 30.0, 'Bills', (today - timedelta(days=30)).isoformat(), '30 days ago')
        db.close()

    response = auth_client.get('/profile')
    assert response.status_code == 200
    # Check that all three expenses appear in the transactions list
    assert b'Today' in response.data
    assert b'5 days ago' in response.data
    assert b'30 days ago' in response.data
    # Check total sum: 10+20+30 = 60
    assert '₹60.00' in response.data.decode('utf-8')
    assert b'3 transactions' in response.data

def _preset_ranges():
    """Calculate expected preset ranges based on today (matches app.py logic)."""
    today = date.today()
    this_month_start = today.replace(day=1)
    this_month_end = today
    last_3m_start = today - relativedelta(months=3)
    last_3m_end = today
    last_6m_start = today - relativedelta(months=6)
    last_6m_end = today
    return [
        ('This Month', this_month_start.isoformat(), this_month_end.isoformat()),
        ('Last 3 Months', last_3m_start.isoformat(), last_3m_end.isoformat()),
        ('Last 6 Months', last_6m_start.isoformat(), last_6m_end.isoformat()),
        ('All Time', None, None)  # No query params
    ]

@pytest.mark.parametrize('preset_name,date_from,date_to', _preset_ranges())
def test_profile_preset_filters(auth_client, preset_name, date_from, date_to):
    """Each preset button filters expenses to the correct date range."""
    today = date.today()
    # Insert expenses: one inside range, one outside
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        # Inside range: today
        insert_expense(db, user_id, 100.0, 'Food', today.isoformat(), 'Inside')
        # Outside range: far past
        insert_expense(db, user_id, 50.0, 'Transport', (today - timedelta(days=400)).isoformat(), 'Outside')
        db.close()

    params = {}
    if date_from and date_to:
        params = {'date_from': date_from, 'date_to': date_to}
    response = auth_client.get('/profile', query_string=params)
    assert response.status_code == 200
    # Inside expense should appear
    assert b'Inside' in response.data
    assert '₹100.00' in response.data.decode('utf-8')  # Amount formatted
    # Outside expense should NOT appear
    assert b'Outside' not in response.data
    assert '₹50.00' not in response.data.decode('utf-8')
    # Check total reflects only inside expense
    assert '₹100.00' in response.data.decode('utf-8')
    assert b'1 transactions' in response.data

def test_profile_custom_range_filtering(auth_client):
    """Submitting a custom date range shows only expenses within that range."""
    today = date.today()
    start = (today - timedelta(days=10)).isoformat()
    end = (today - timedelta(days=5)).isoformat()
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        # Inside range
        insert_expense(db, user_id, 15.0, 'Food', (today - timedelta(days=7)).isoformat(), 'Inside')
        # Outside range (too early)
        insert_expense(db, user_id, 25.0, 'Transport', (today - timedelta(days=20)).isoformat(), 'Too early')
        # Outside range (too late)
        insert_expense(db, user_id, 35.0, 'Bills', today.isoformat(), 'Too late')
        db.close()

    response = auth_client.get('/profile', query_string={'date_from': start, 'date_to': end})
    assert response.status_code == 200
    assert b'Inside' in response.data
    assert b'Too early' not in response.data
    assert b'Too late' not in response.data
    assert '₹15.00' in response.data.decode('utf-8')
    assert b'1 transactions' in response.data

def test_profile_invalid_range_shows_error_and_fallback(auth_client):
    """Submitting range where date_from > date_to shows flash error and falls back to unfiltered."""
    today = date.today()
    start = today.isoformat()
    end = (today - timedelta(days=10)).isoformat()  # start > end
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        insert_expense(db, user_id, 100.0, 'Food', today.isoformat(), 'Expense')
        db.close()

    response = auth_client.get('/profile', query_string={'date_from': start, 'date_to': end}, follow_redirects=True)
    assert response.status_code == 200
    # Check for flash error message
    assert b'Start date must be before end date.' in response.data
    # Should show the expense (fallback to unfiltered)
    assert b'Expense' in response.data
    assert '₹100.00' in response.data.decode('utf-8')

def test_profile_malformed_dates_do_not_crash(auth_client):
    """Submitting malformed date strings does not crash; falls back to unfiltered."""
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        insert_expense(db, user_id, 50.0, 'Food', date.today().isoformat(), 'Expense')
        db.close()

    # Test various malformed inputs
    malformed_values = ['not-a-date', '2026-13-01', '2026-02-30', '', '2026/01/01']
    for bad in malformed_values:
        response = auth_client.get('/profile', query_string={'date_from': bad, 'date_to': bad})
        assert response.status_code == 200  # Should not crash
        # Should show the expense (fallback to unfiltered)
        assert b'Expense' in response.data
        assert '₹50.00' in response.data.decode('utf-8')

def test_profile_active_filter_indicators(auth_client):
    """Active preset button or custom-range fields visually indicate which filter is applied."""
    today = date.today()
    # This Month preset
    this_month_start = today.replace(day=1).isoformat()
    this_month_end = today.isoformat()
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        insert_expense(db, user_id, 10.0, 'Food', today.isoformat(), 'Expense')
        db.close()

    response = auth_client.get('/profile', query_string={
        'date_from': this_month_start,
        'date_to': this_month_end
    })
    assert response.status_code == 200
    # Check that the preset button for "This Month" has an active state
    # Assuming the template adds a class "active" to the button when matches
    assert b'This Month' in response.data
    # Check that the inputs are populated with the correct values
    assert f'value="{this_month_start}"'.encode() in response.data
    assert f'value="{this_month_end}"'.encode() in response.data

def test_profile_rupee_symbol_persists(auth_client):
    """All amounts continue to display ₹ symbol regardless of active filter."""
    today = date.today()
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        insert_expense(db, user_id, 99.99, 'Food', today.isoformat(), 'Expense')
        db.close()

    # Test unfiltered
    resp = auth_client.get('/profile')
    assert '₹99.99' in resp.data.decode('utf-8')
    # Test filtered
    resp = auth_client.get('/profile', query_string={
        'date_from': today.isoformat(),
        'date_to': today.isoformat()
    })
    assert '₹99.99' in resp.data.decode('utf-8')

def test_profile_zero_state_when_no_matching_expenses(auth_client):
    """User with no expenses in selected range sees ₹0.00 total, 0 transactions, empty breakdown."""
    today = date.today()
    # Insert an expense far in the past
    with flask_app.app_context():
        db = get_db()
        user_id = 1
        insert_expense(db, user_id, 100.0, 'Food', (today - timedelta(days=400)).isoformat(), 'Old expense')
        db.close()

    # Request a range that excludes the expense (e.g., last 7 days)
    start = (today - timedelta(days=7)).isoformat()
    end = today.isoformat()
    response = auth_client.get('/profile', query_string={'date_from': start, 'date_to': end})
    assert response.status_code == 200
    assert '₹0.00' in response.data.decode('utf-8')
    assert b'0 transactions' in response.data
    # Check that no expense amounts appear in breakdown
    assert '₹100.00' not in response.data.decode('utf-8')