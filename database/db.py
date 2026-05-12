import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'

def get_db():
    """
    Returns a SQLite connection with row_factory and foreign keys enabled.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates all tables using CREATE TABLE IF NOT EXISTS.
    """
    conn = get_db()

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
    conn = get_db()

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
