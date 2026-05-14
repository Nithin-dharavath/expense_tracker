import sqlite3
import os
from flask import current_app, g
from werkzeug.security import generate_password_hash

def get_db():
    """
    Returns a SQLite connection with row_factory and foreign keys enabled.
    Uses flask.g to persist the connection during a request.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    """
    Closes the database connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def _get_db_path():
    """
    Helper to get the database path from the app config or fallback to default.
    """
    try:
        return current_app.config['DATABASE']
    except RuntimeError:
        return 'spendly.db'

def init_db():
    """
    Creates all tables using CREATE TABLE IF NOT EXISTS.
    """
    # We use a direct connection here because we might not be in a request context
    # or we want to ensure the tables are created in the correct DB file/memory.
    # If we are in a request context, use get_db(), otherwise use config.
    db_path = _get_db_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    # Create expenses table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

def seed_db():
    """
    Inserts sample data for development. Prevents duplication.
    """
    db_path = _get_db_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    # Check if users table already contains data
    user_exists = conn.execute('SELECT 1 FROM users LIMIT 1').fetchone()
    if user_exists:
        conn.close()
        return

    # Insert demo user
    demo_password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ("Demo User", "demo@spendly.com", demo_password_hash)
    )
    demo_user_id = cursor.lastrowid

    # Sample expenses across all required categories
    sample_expenses = [
        (demo_user_id, 12.50, 'Food', '2026-05-01', 'Lunch at cafe'),
        (demo_user_id, 45.00, 'Transport', '2026-05-02', 'Gas refill'),
        (demo_user_id, 120.00, 'Bills', '2026-05-03', 'Electricity bill'),
        (demo_user_id, 30.00, 'Health', '2026-05-04', 'Pharmacy'),
        (demo_user_id, 60.00, 'Entertainment', '2026-05-05', 'Movie tickets'),
        (demo_user_id, 85.20, 'Shopping', '2026-05-06', 'New shirt'),
        (demo_user_id, 15.00, 'Other', '2026-05-07', 'Parking fee'),
        (demo_user_id, 22.10, 'Food', '2026-05-08', 'Dinner'),
    ]

    conn.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        sample_expenses
    )

    conn.commit()
    conn.close()
