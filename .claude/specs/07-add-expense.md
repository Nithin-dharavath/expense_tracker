---
# Spec: Add Expense

## Overview
This feature allows logged-in users to record(add) new expenses. Users will provide the amount, category, date, and an optional description. This is a core part of the Expense CRUD functionality, enabling users to track their spending over time.

## Depends on
- 03-login-and-logout

## Routes
- `GET /expenses/add` — Render the add expense form — logged-in
- `POST /expenses/add` — Process the form submission and save the expense to the DB — logged-in

## Database changes
No database changes.

## Templates
- **Create:** `templates/add_expense.html`
- **Modify:** `templates/base.html` (add link to the add expense page)

## Files to change
- `app.py`
- `templates/base.html`

## Files to create
- `templates/add_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- User can navigate to `/expenses/add` while logged in.
- Guest users are redirected to the login page when accessing `/expenses/add`.
- Form correctly captures amount, category, date, and description.
- Submitted expenses are correctly inserted into the `expenses` table with the current `user_id`.
- User is redirected to the profile page after successful submission.
- Form displays errors for invalid input (e.g., negative amount, missing required fields).
---
