---
# Spec: Backend Routes for Profile Page

## Overview
This feature replaces the mock data in the `/profile` route with real data fetched from the database. It ensures that users see their own profile details, calculated spending statistics, and their actual transaction history.

## Depends on
- 01-database-setup
- 03-login-and-logout

## Routes
- `GET /profile` — Fetch and display user profile, spending stats, and transaction history — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` — Update to use dynamic data passed from the route instead of mock data.

## Files to change
- `app.py`

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
- [ ] Logged-in users see their correct name and email on the profile page.
- [ ] Total spent is correctly calculated as the sum of all expenses for the logged-in user.
- [ ] Transaction count matches the number of expenses for the logged-in user.
- [ ] Top category is correctly identified as the category with the highest total spend.
- [ ] Category breakdown lists all categories the user has spent in with their corresponding total and percentage.
- [ ] Transaction list shows the user's actual expenses from the database, sorted by date descending.
- [ ] Unauthenticated users are redirected to the login page when accessing `/profile`.
---