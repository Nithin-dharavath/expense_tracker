# 💸 Spendly - Personal Expense Tracker

Spendly is a clean, professional, and efficient personal finance management tool built with Flask. It allows users to track their spending, categorize expenses, and gain insights into their financial habits through a personalized dashboard.

## ✨ Features

### 🔐 User Authentication
- **Secure Onboarding**: User registration and login system with password hashing using `Werkzeug`.
- **Session Management**: Secure session-based authentication to protect user data.
- **Profile Customization**: Dynamic user avatars generated based on user names via the DiceBear API.

### 📊 Expense Management (CRUD)
- **Track Spending**: Easily add new expenses with amount, category, date, and optional descriptions.
- **Edit & Manage**: Full capability to update or delete existing transactions.
- **Categorization**: Pre-defined categories (Food, Transport, Bills, Health, Entertainment, Shopping, Other) to organize spending.

### 📈 Insights & Analytics
- **Financial Dashboard**: A comprehensive profile view showing total spending, total transaction count, and the top spending category.
- **Category Breakdown**: Visual summary of spending across different categories.
- **Smart Filtering**: Filter expenses by custom date ranges or use quick-presets:
  - This Month
  - Last 3 Months
  - Last 6 Months
- **Recent Transactions**: A chronological list of the latest expenses for quick review.

### 🛡️ Legal & Trust
- Dedicated **Terms of Service** and **Privacy Policy** pages to ensure transparency.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+ / [Flask](https://flask.palletsprojects.com/)
- **Database**: [SQLite](https://www.sqlite.org/) (Relational storage with foreign key constraints)
- **Frontend**: Jinja2 Templates, HTML5, CSS3, JavaScript
- **Security**: `Werkzeug` for password hashing
- **Testing**: `pytest` and `pytest-flask`
- **Utilities**: `python-dateutil` for advanced date manipulations

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Flask development server:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5001`.

### Running Tests
The project includes a suite of functional tests to ensure stability.
```bash
pytest
```

---

## 📂 Project Structure

```text
expense-tracker/
├── app.py              # Main application entry point & route definitions
├── database/           # Database layer
│   ├── db.py          # Connection handling, initialization, and seeding
│   └── queries.py     # Modular SQL queries for business logic
├── static/            # Static assets
│   ├── css/           # Stylesheets (style.css, profile.css)
│   └── js/            # Client-side logic (main.js)
├── templates/          # Jinja2 HTML templates
│   ├── base.html      # Shared layout wrapper
│   ├── profile.html   # User dashboard and analytics
│   ├── add_expense.html # Expense creation form
│   └── ...             # Other view templates
├── tests/              # Pytest test suite
└── requirements.txt    # Project dependencies
```

---

## 🗄️ Database Schema

The application uses a lightweight SQLite database (`spendly.db`) with two primary tables:

### `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY | Unique user identifier |
| `name` | TEXT | NOT NULL | User's full name |
| `email` | TEXT | UNIQUE, NOT NULL | Registered email address |
| `password_hash`| TEXT | NOT NULL | Securely hashed password |
| `created_at` | TEXT | DEFAULT now() | Account creation timestamp |

### `expenses`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY | Unique expense identifier |
| `user_id` | INTEGER | FK (users.id) | Reference to the user |
| `amount` | REAL | NOT NULL | Transaction amount |
| `category` | TEXT | NOT NULL | Expense category |
| `date` | TEXT | NOT NULL | Date of transaction (YYYY-MM-DD) |
| `description` | TEXT | - | Optional transaction note |
| `created_at` | TEXT | DEFAULT now() | Record creation timestamp |

---

## 🗺️ Roadmap
- [ ] **Export Data**: Ability to export expenses to CSV/PDF.
- [ ] **Budgeting**: Set monthly budget limits and receive alerts.
- [ ] **Advanced Visualization**: Integrate Chart.js for graphical spending trends.
- [ ] **Multi-Currency Support**: Convert expenses between different currencies.

## 📄 License
This project is licensed under the MIT License.
