from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database.db import init_db, seed_db, get_db
from database.queries import get_summary_stats, get_recent_transactions, get_category_breakdown
from functools import wraps
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.secret_key = "spendly-super-secret-key"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

with app.app_context():
    init_db()
    seed_db()



# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not email or not password or not confirm_password:
            return render_template("register.html", error="All fields are required.")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match.")

        hashed_pw = generate_password_hash(password)

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hashed_pw)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="This email is already registered.")
        finally:
            db.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        user = db.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,)).fetchone()
        db.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("landing"))

        return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    return redirect(url_for("landing"))


@app.route("/profile")
@login_required
def profile():
    user_id = session.get("user_id")

    # Date Filtering Logic
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    # Validate dates
    def validate_date(d):
        if not d: return None
        try:
            return datetime.strptime(d, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None

    date_from = validate_date(date_from)
    date_to = validate_date(date_to)

    if date_from and date_to and date_from > date_to:
        flash("Start date must be before end date.")
        date_from = date_to = None

    # Fetch User Profile
    db = get_db()
    user_row = db.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    db.close()

    # Fetch data using query helpers
    stats_row = get_summary_stats(user_id, date_from, date_to)
    total_spent_val = stats_row["total_spent"] if stats_row and stats_row["total_spent"] is not None else 0.0
    transaction_count = stats_row["transaction_count"] if stats_row else 0

    categories_rows = get_category_breakdown(user_id, date_from, date_to)

    category_breakdown = []
    top_category = "N/A"

    for i, row in enumerate(categories_rows):
        category = row["category"]
        amount = row["total"]
        percentage = (amount / total_spent_val * 100) if total_spent_val > 0 else 0

        if i == 0:
            top_category = category

        category_breakdown.append({
            "category": category,
            "amount": f"₹{amount:.2f}",
            "percentage": round(percentage, 1)
        })

    transactions_rows = get_recent_transactions(user_id, date_from=date_from, date_to=date_to)

    user_profile = {
        "user": {
            "name": user_row["name"],
            "email": user_row["email"],
            "join_date": user_row["created_at"],
            "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_row['name']}"
        },
        "stats": {
            "total_spent": f"₹{total_spent_val:.2f}",
            "transaction_count": transaction_count,
            "top_category": top_category
        },
        "category_breakdown": category_breakdown,
        "transactions": [
            {
                "date": row["date"],
                "description": row["description"],
                "category": row["category"],
                "amount": f"-₹{row['amount']:.2f}"
            }
            for row in transactions_rows
        ]
    }
    # Calculate presets for the template
    today = date.today()
    this_month_start = today.replace(day=1).isoformat()
    this_month_end = today.isoformat()

    last_3m_start = (today - relativedelta(months=3)).isoformat()
    last_3m_end = today.isoformat()

    last_6m_start = (today - relativedelta(months=6)).isoformat()
    last_6m_end = today.isoformat()

    return render_template(
        "profile.html",
        profile=user_profile,
        date_from=date_from,
        date_to=date_to,
        this_month_start=this_month_start,
        this_month_end=this_month_end,
        last_3m_start=last_3m_start,
        last_3m_end=last_3m_end,
        last_6m_start=last_6m_start,
        last_6m_end=last_6m_end
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)