from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database.db import init_db, seed_db, get_db
from functools import wraps

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
    mock_user_profile = {
        "user": {
            "name": "Nitin Sharma",
            "email": "nitin.sharma@example.com",
            "join_date": "January 12, 2024",
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Nitin"
        },
        "stats": {
            "total_spent": "₹12,450.00",
            "transaction_count": 42,
            "top_category": "Dining"
        },
        "category_breakdown": [
            {"category": "Dining", "amount": "₹4,200", "percentage": 33.7},
            {"category": "Transport", "amount": "₹3,100", "percentage": 24.9},
            {"category": "Grocery", "amount": "₹2,800", "percentage": 22.5},
            {"category": "Entertainment", "amount": "₹2,350", "percentage": 18.9},
        ],
        "transactions": [
            {"date": "2024-05-12", "description": "Starbucks Coffee", "category": "Dining", "amount": "-₹450.00"},
            {"date": "2024-05-11", "description": "Uber Ride", "category": "Transport", "amount": "-₹220.00"},
            {"date": "2024-05-10", "description": "Amazon Fresh", "category": "Grocery", "amount": "-₹1,200.00"},
            {"date": "2024-05-08", "description": "Netflix Monthly", "category": "Entertainment", "amount": "-₹499.00"},
            {"date": "2024-05-05", "description": "Local Restaurant", "category": "Dining", "amount": "-₹850.00"},
        ]
    }
    return render_template("profile.html", profile=mock_user_profile)


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