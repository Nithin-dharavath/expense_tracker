---
# Spec: Login and Logout

## Overview
This feature implements the authentication mechanism for Spendly, allowing registered users to access their accounts and securely log out. It ensures that users can only access protected areas of the application after verifying their credentials.

## Depends on
- 02-registration

## Routes
- `GET /login` — Display login form — public
- `POST /login` — Authenticate user and start session — public
- `GET /logout` — Terminate user session — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `login.html` — Implement the login form and handle error messages.
- **Modify:** `base.html` — Update navigation to show "Login/Register" when logged out and "Logout/Profile" when logged in.

## Files to change
- `app.py` — Implement login/logout logic and session management.

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
- Use Flask `session` for managing the logged-in state

## Definition of done
- [ ] User can see the login page at `/login`.
- [ ] User can successfully log in with registered credentials and is redirected to the profile page.
- [ ] User sees an error message when attempting to log in with invalid credentials.
- [ ] User is redirected to the login page when attempting to access `/logout` or `/profile` while not authenticated.
- [ ] Logged-in users see a "Logout" link in the navigation bar.
- [ ] Clicking "Logout" clears the session and redirects the user to the landing page.
---
