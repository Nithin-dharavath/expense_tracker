---
# Spec: Delete Expense

## Overview
The Delete Expense feature allows users to remove unwanted or incorrect expense records from their history. This completes the basic CRUD (Create, Read, Update, Delete) cycle for expenses, providing users with full control over their financial data.

## Depends on
- `01-database-setup`
- `03-login-and-logout`
- `07-add-expense`
- `08-edit-expense`

## Routes
- `POST /expenses/<int:id>/delete` — Deletes a specific expense record. Access: logged-in.

## Database changes
No database schema changes. A new query function `delete_expense(expense_id, user_id)` will be added to `database/queries.py` to ensure expenses can only be deleted by their owner.

## Templates
- **Modify:** `templates/profile.html` — Add a "Delete" button/link next to each transaction in the recent transactions list. This should be implemented as a small form to perform a `POST` request for security.

## Files to change
- `app.py`
- `database/queries.py`
- `templates/profile.html`

## Files to create
- No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Ensure an expense cannot be deleted by a user who doesn't own it (validate `user_id` in the query).
- Use a `POST` method for the deletion to prevent accidental deletions via crawler or simple link clicking.
- Provide a success flash message after deletion.

## Definition of done
- [ ] An "Action" or "Delete" button exists for every expense on the profile page.
- [ ] Clicking "Delete" removes the expense from the database.
- [ ] The user is redirected back to the profile page after deletion.
- [ ] A flash message "Expense deleted successfully" appears after a successful delete.
- [ ] Attempting to delete an expense that doesn't exist or belongs to another user returns a 404 error or a failure flash message.
- [ ] The "Total Spent" and "Transaction Count" stats on the profile page update immediately after a deletion.
---
