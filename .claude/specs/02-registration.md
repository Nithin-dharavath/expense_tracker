---
# Spec: Registration

## Overview
This feature allows new users to create an account on Spendly by providing their name, email, and password. This is a foundational step in the roadmap, enabling personalized expense tracking by establishing the user identity required for all subsequent features.

## Depends on
None (Initial user management step).

## Routes
- `GET /register` — Display the registration form — public
- `POST /register` — Handle registration form submission and create user account — public

## Database changes
No database changes. The `users` table already exists with `id`, `name`, `email`, and `password_hash`.

## Templates
- **Create:** None (Existing `register.html` will be used)
- **Modify:** `templates/register.html` — Implement the HTML form with appropriate input fields and error messaging.

## Files to change
- `app.py` — Implement the `POST /register` route and update the `GET /register` route to handle validation errors.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] A user can successfully register with a name, email, and password.
- [ ] Registration fails and shows an error if the email is already taken (UNIQUE constraint).
- [ ] Registration fails if any required field is missing.
- [ ] Passwords are stored as hashes in the database, not plain text.
- [ ] Successful registration redirects the user to the login page or logs them in automatically.
---
