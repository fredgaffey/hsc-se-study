# Year 12 AT1: Secure Software

The first Year 12 assessment: take **Small-Brain**, a deliberately insecure Flask quiz app, and secure it in three stages.

1. **Basic:** password hashing and salting, input validation on every API route, sanitising inputs against XSS
2. **Session management:** cryptographically secure session tokens, validating them on protected routes, moving from localStorage to sessionStorage
3. **CSRF:** double-token CSRF protection, HTTP-only session cookies, CSRF checks on state-changing requests

| | |
|---|---|
| `code/` | My final submitted code (Flask back end + front end). `code/README.md` has the full brief; `SPECIFICATIONS.md`, `TESTING.md` and `DOCUMENTATION.md` are inside it |
| [documentation/AT1 documentation (final).docx](documentation/AT1%20documentation%20(final).docx) | Final documentation |
| `documentation/OWASP ZAP scan session.zip` | The OWASP ZAP security-testing session (open it in ZAP) |

**If you're doing this assessment yourself, do it yourself first.** Read this afterwards, to compare approaches. Submitting someone else's work is an academic integrity breach.
