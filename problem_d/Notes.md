# Pull Request Review Findings

## Summary of Changes

1. **Frontend (main.ts, styles.css):**
   - Added an "Audit log" dashboard card with a button to trigger audit events.
   - Fetches audit log entries from `/api/usage/audit-log` and displays them.
   - Button triggers POST to `/api/usage/audit` and updates log.
   - Minor CSS update for button alignment.

2. **Backend (audit_writer, usage.controller.ts, usage.service.ts):**
   - Added vendor binary `audit_writer` for writing audit events.
   - New endpoints:
     - `GET /usage/audit-log`: Returns last 10 audit log entries.
     - `POST /usage/audit`: Validates and records audit event using binary.
   - Service uses child process to call binary and update DB.
   - Error handling for invalid messages and binary failures.

3. **Database (schema.sql, seed.sql):**
   - Added `audit_log` table (id, event, created_at).
   - Seeded with initial audit event.

4. **Documentation:**
   - Updated backend README to mention new endpoints.
   - Minor cleanup in main README.

## Findings

- **Security:**
  - Audit event input is validated for length and emptiness.
  - Binary execution errors are handled and surfaced as forbidden.
- **Reliability:**
  - Audit log fetch is limited to 10 most recent entries.
  - Frontend gracefully handles API failures.
- **Maintainability:**
  - Vendor binary is used for DB writes; source not reviewed.
  - Clear separation between frontend, backend, and DB changes.

## Follow-up Questions

1. Is the vendor binary `audit_writer` open source or auditable? Any documentation?
2. How are audit log IDs generated and are they guaranteed unique?
3. Is there a risk of injection or abuse via the audit event message?
4. Should audit log entries be paginated or exportable for larger logs?
5. Is there a retention policy for audit logs?
6. Are there tests for the new endpoints and binary integration?
7. Should audit events be triggered for more actions (not just manual button)?
8. Is the audit log visible to all users or restricted by role?
9. Is the frontend error handling sufficient for production?
10. Is the backend binary execution cross-platform (Windows, Linux)?

---
End of review.
