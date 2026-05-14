---
# Spec: Edit Expense

## Overview
Allow users to modify existing expense records. This feature ensures that users can correct mistakes or update details of their transactions, providing a complete CRUD experience for expense management.

## Depends on
- 07-add-expense

## Routes
- `GET /expenses/<int:id>/edit` — Displays the edit form pre-filled with the expense's current data — logged-in
- `POST /expenses/<int:id>/edit` — Processes the updated expense data and saves it to the database — logged-in

## Database changes
No database changes. A new helper function `update_expense` will be added to `database/queries.py`.

## Templates
- **Create:** `templates/edit_expense.html` (similar to `add_expense.html`, pre-filled with current values)
- **Modify:** No existing templates modified.

## Files to change
- `app.py`: Implement the `edit_expense` route with GET and POST handlers.
- `database/queries.py`: Add `get_expense_by_id` and `update_expense` functions.

## Files to create
- `templates/edit_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- **Authorization:** Ensure the expense being edited belongs to the currently logged-in user. If the user attempts to edit an expense they don't own, return a 403 Forbidden or 404 Not Found.

## Definition of done
- [ ] Navigate to `/expenses/<id>/edit` for an owned expense and see a pre-filled form.
- [ ] Navigate to `/expenses/<id>/edit` for an unowned expense and receive an error (403/404).
- [ ] Successfully update an expense's amount, category, date, and description.
- [ ] Verify that the updated values are reflected on the profile page.
- [ ] Form validation: Ensure amount is positive and date is valid, similar to the "Add Expense" feature.
- [ ] Incorrect category or invalid data prevents the update and shows an error message.
---
