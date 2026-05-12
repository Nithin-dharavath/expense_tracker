# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands
- Run application: `python app.py` (runs on port 5001)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest`

## Architecture and Structure
The project is a Flask-based expense tracker application.

- `app.py`: Main entry point containing route definitions and application configuration.
- `database/`: Contains database logic.
  - `db.py`: Intended for database connection (`get_db`), initialization (`init_db`), and seeding (`seed_db`) using SQLite.
- `templates/`: Contains Jinja2 HTML templates for the frontend.
- `static/`: Stores static assets (CSS, JS, images).
- `requirements.txt`: Project dependencies.

The current state of the project is a skeleton/starter kit where several core features (Authentication, Profile, Expense CRUD) are defined as placeholder routes and need implementation.
