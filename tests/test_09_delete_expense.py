import pytest
import os
from flask import url_for, session
from app import app as flask_app
from database.db import init_db, get_db

@pytest.fixture
def app():
    db_path = 'test_spendly.db'
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })
    with flask_app.app_context():
        init_db()
        yield flask_app
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in as a test user."""
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    return client

class TestDeleteExpense:
    def test_delete_expense_happy_path(self, auth_client, app):
        """Test that a user can successfully delete their own expense."""
        with app.app_context():
            db = get_db()
            user_id = session.get("user_id") if session else 1 # In test client, session is handled differently
            # Since we are outside the request in the fixture, we need to get user_id from DB
            user = db.execute("SELECT id FROM users LIMIT 1").fetchone()
            user_id = user['id']

            # Create an expense for this user
            cursor = db.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                (user_id, 50.0, 'Food', '2026-05-15', 'Test Expense')
            )
            expense_id = cursor.lastrowid
            db.commit()

            delete_url = f'/expenses/{expense_id}/delete'

        # Perform deletion
        response = auth_client.post(delete_url, follow_redirects=False)

        # Verify redirect to profile
        assert response.status_code == 302
        assert response.location == url_for('profile', _external=False)

        # Verify success flash message (requires following redirect or checking session)
        response = auth_client.get(url_for('profile'))
        assert b"Expense deleted successfully" in response.data

        # Verify DB side effect: record is gone
        with app.app_context():
            db = get_db()
            expense = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
            assert expense is None, "Expense should have been deleted from database"

    def test_delete_expense_auth_guard(self, client):
        """Test that unauthenticated users cannot delete expenses."""
        # Attempt to delete expense 1 without logging in
        response = client.post('/expenses/1/delete', follow_redirects=False)

        # Should redirect to login page
        assert response.status_code == 302
        assert response.location == url_for('login', _external=False)

    def test_delete_expense_ownership_guard(self, client, app):
        """Test that a user cannot delete an expense belonging to another user."""
        # Create User A
        client.post('/register', data={'name': 'User A', 'email': 'a@test.com', 'password': 'passwordA', 'confirm_password': 'passwordA'})

        # Create User B
        client.post('/register', data={'name': 'User B', 'email': 'b@test.com', 'password': 'passwordB', 'confirm_password': 'passwordB'})

        with app.app_context():
            db = get_db()
            # Get User B's ID
            user_b = db.execute("SELECT id FROM users WHERE email = ?", ('b@test.com',)).fetchone()
            user_b_id = user_b['id']

            # Create expense for User B
            cursor = db.execute(
                "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                (user_b_id, 100.0, 'Bills', '2026-05-15', 'User B Expense')
            )
            expense_id = cursor.lastrowid
            db.commit()

        # Log in as User A
        client.post('/login', data={'email': 'a@test.com', 'password': 'passwordA'})

        # Attempt to delete User B's expense
        response = client.post(f'/expenses/{expense_id}/delete')

        # Should return 404 as per spec
        assert response.status_code == 404

    def test_delete_expense_non_existent(self, auth_client):
        """Test that attempting to delete a non-existent expense returns 404."""
        # Use an ID that definitely doesn't exist
        response = auth_client.post('/expenses/99999/delete')

        assert response.status_code == 404

    def test_delete_expense_method_guard(self, auth_client):
        """Test that GET requests to the delete endpoint are not allowed."""
        # We don't need to know if the expense exists, the method should be blocked first
        response = auth_client.get('/expenses/1/delete')

        # Flask returns 405 by default for missing methods in route definition
        assert response.status_code == 405
