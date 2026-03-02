<!-- # Add user display lookup for dashboard

**Closes #88** — Show user name in dashboard header

---

## Summary

The dashboard header currently shows a placeholder. This PR wires it to the user API so we display the logged-in user's name and role (e.g. `Jane Doe (admin)`).

The support tool also needs to resolve users by email; `lookup_by_email` is added for that. It's used internally only and is not exposed to the front end.

---

## What changed

- `**user_helpers.py`** — New helpers:
  - `get_user_display(user_id)` — fetches name and email for a user
  - `get_user_list(role=None)` — fetches users, optional role filter
  - `format_user_for_header(user_id)` — returns `"Name"` or `"Name (role)"` for the dashboard header
  - `lookup_by_email(email)` — returns user id for support tool; used server-side only

---

## Constraints & requirements

- **Do not expose internal user IDs** to the front end (e.g. UUIDs, internal PKs). The header should show only display name and role.
- **API calls must timeout** after 2 seconds. The dashboard must not block on slow external calls.
- **Keep the dashboard responsive.** Avoid extra API calls or unnecessary work in the hot path.
- **Authentication** is handled upstream (API gateway). Input validation for user IDs happens at the gateway. This module assumes valid, authenticated requests.

---

## Out of scope

- Refactoring unrelated modules
- Changing the external user API contract
- Adding new auth or session logic
- Formatting or style-only changes (unless they affect correctness)

---

## Testing

- Manual check: dashboard header shows correct name and role for logged-in user
- `lookup_by_email` returns correct id for known emails, `None` for unknown
- Role filter works in `get_user_list`
 -->

# Add user display lookup for dashboard header

---

## Overview

The dashboard header currently displays a placeholder value instead of the logged-in user's name.

This PR integrates the external User API to retrieve and display:

- The user’s full name
- The user’s role (if present)

Example display:

Jane Doe (admin)

Additionally, this PR introduces a server-side helper for resolving users by email for use in the internal support tool.

---

## Changes Introduced

### `user_helpers.py` (new module)

Added the following helper functions:

- `get_user_display(user_id)`
  - Fetches name and role for a given user ID.

- `get_user_list(role=None)`
  - Retrieves all users.
  - Optional role filter (e.g., `admin`, `support`).

- `format_user_for_header(user_id)`
  - Returns formatted display string:
    - `"Name"`
    - `"Name (role)"`

- `lookup_by_email(email)`
  - Returns user ID for a given email.
  - Used by the internal support tool only.
  - Not exposed to the front end.

---

## Constraints & Requirements

- Do **not expose internal user IDs** (UUIDs, PKs) to the front end.
- All external API calls must:
  - Timeout after **2 seconds**
  - Avoid blocking the dashboard render
- Keep the dashboard responsive:
  - Avoid redundant or unnecessary API calls
- Authentication and input validation are handled upstream (API gateway).

---

## Out of Scope

- Refactoring unrelated modules
- Changing the external User API contract
- Modifying authentication/session logic
- Style-only formatting changes (unless correctness-related)

---

## Testing

### Manual

- Dashboard header shows correct name for logged-in user.
- Role is displayed when present.
- No user ID values appear in UI.

### Functional

- `lookup_by_email(email)`:
  - Returns correct ID for known email
  - Returns `None` for unknown email

- `get_user_list(role="admin")`:
  - Returns only users with matching role

---

## Risk & Impact

- Introduces dependency on external User API in dashboard render path.
- Potential performance impact if API latency increases.
- Must ensure timeout handling and graceful degradation.

---
