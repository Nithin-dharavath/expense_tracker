from database.db import get_db

def create_expense(user_id, amount, category, date, description):
    """
    Inserts a new expense into the database.
    """
    db = get_db()
    db.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, date, description)
    )
    db.commit()

def get_summary_stats(user_id, date_from=None, date_to=None):
    db = get_db()
    query = "SELECT SUM(amount) as total_spent, COUNT(id) as transaction_count FROM expenses WHERE user_id = ?"
    params = [user_id]

    if date_from and date_to:
        query += " AND date BETWEEN ? AND ?"
        params.extend([date_from, date_to])

    row = db.execute(query, params).fetchone()
    return row

def get_recent_transactions(user_id, limit=10, date_from=None, date_to=None):
    db = get_db()
    query = "SELECT date, description, category, amount FROM expenses WHERE user_id = ?"
    params = [user_id]

    if date_from and date_to:
        query += " AND date BETWEEN ? AND ?"
        params.extend([date_from, date_to])

    query += " ORDER BY date DESC LIMIT ?"
    params.append(limit)

    rows = db.execute(query, params).fetchall()
    return rows

def get_category_breakdown(user_id, date_from=None, date_to=None):
    db = get_db()
    query = "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ?"
    params = [user_id]

    if date_from and date_to:
        query += " AND date BETWEEN ? AND ?"
        params.extend([date_from, date_to])

    query += " GROUP BY category ORDER BY total DESC"

    rows = db.execute(query, params).fetchall()
    return rows
