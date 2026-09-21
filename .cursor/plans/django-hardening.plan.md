---
name: Django hardening and cleanup
overview: Sequenced implementation of the 20 Sep 2026 audit. Lock down finance auth, private receipts, and prod settings first. Then security headers, unused deps, leftover query cost, and a separate upgrade branch for Python/Django/MySQL.
todos:
  - id: staff-gate-fidouche
    content: Staff-gate every fidouche view; add a non-staff 403/302 test
    status: pending
  - id: private-receipts
    content: Stop serving /uploads/receipts publicly; login-gated download
    status: pending
  - id: ssn-fields
    content: Encrypt or remove SSN fields; lock down Member/Sub admin
    status: pending
  - id: prod-settings
    content: Commit sanitized prod.py; fail if SECRET_KEY is missing
    status: pending
  - id: security-headers
    content: Add SecurityMiddleware, SECURE_*, and nginx proto/headers
    status: pending
  - id: split-requirements
    content: Split requirements-dev.txt; drop unused REST/crypto/localflavor
    status: pending
  - id: leftover-perf
    content: Cache nav context processors; paginate past shows by year
    status: pending
  - id: platform-upgrade
    content: Python 3.12 + Django 4.2, then 5.2 LTS; plan MySQL 5.7 exit
    status: pending
isProject: false
---

# Django hardening and cleanup

Converted from the [Foreverland Django audit](/root/.cursor/projects/workspaces-foreverland-v2/canvases/django-app-audit.canvas.tsx) (20 Sep 2026). Queryset N+1 work, social widgets, and RequireJS removal stay as-is.

Do phases 1–2 before any more performance work. Confirm whether setter accounts are staff-only before changing fidouche auth; the code still allows a non-staff login to read tax reports.

## Phase 1 — Stop the leaks

Authorization and public files. No schema change except optional upload-name randomness.

### 1. Staff-gate fidouche

- Add `@staff_member_required` (or a dedicated finance group) to every view in `web/fidouche/views.py`. Writes are already staff-gated; reads are not (`financial_dashboard`, `tax_reports`, `gig_finances_view`, payment lists).
- Keep setter on `@login_required`.
- Test: non-staff user gets 302/403 on `/fidouche/tax-reports/` and `/fidouche/`. Staff still sees totals from the existing query-budget fixtures.

### 2. Private receipts

- Nginx currently aliases `/uploads` → media volume with no auth. `Expense.receipt_img` and `Show.settlement_sheet` land under `receipts/`.
- Serve receipts through a staff view. Keep public photos/posters on a separate prefix (`images/`, `venues/`, `posters/`).
- Restrict uploads to image/pdf and cap size in `web/fidouche/forms.py`. Prefer random stored names.
- Set `X-Content-Type-Options: nosniff` on the remaining public media location.

### 3. SSN fields

- Plaintext `CharField` SSNs on `Member`, `Sub`, `Payee`, `Agent`, `ProductionCompany`, `Fiduciary`. Default `ModelAdmin` shows them to any staff user.
- Decide: encrypt at rest (Fernet key from env) or stop storing them. If kept for 1099s, custom admin that masks values and a staff group that can reveal them.
- Never render SSNs in fidouche templates.

### 4. Production settings in git

- `foreverland.wsgi` and `docker-compose.prod.yml` load `foreverland.settings.prod`, but `prod.py` is not in the repo. `base.py` is both tracked and gitignored.
- Commit a sanitized `web/foreverland/settings/prod.py` (no secrets). Fail fast if `SECRET_KEY` is missing. Parse `DEBUG` as a real boolean. Require `DJANGO_ALLOWED_HOSTS`.
- Stop gitignoring `base.py` now that secrets come from env.

## Phase 2 — Request hardening

### 5. Django security middleware

In `web/foreverland/settings/base.py`:

- Insert `SecurityMiddleware` first and `XFrameOptionsMiddleware`.
- Prod only: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`.

### 6. Nginx

In `nginx/nginx.conf`:

- `proxy_set_header X-Forwarded-Proto $scheme;`
- `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` on the TLS server.

### 7. Template XSS

- Drop `|safe` on `show.notes` (`shows/past.html`), quotes (`fidouche/dashboard.html`), and Django messages unless the field is trusted rich text. `linebreaksbr` is enough for notes.

### 8. Stop `migrate --fake-initial` on every boot

- Both compose files run it in the container command. Use `migrate --noinput` only. Fake-initial is a one-off import, not an entrypoint.

## Phase 3 — Dependencies and leftovers

### 9. Split requirements

- `requirements.txt`: runtime only.
- `requirements-dev.txt`: `django-debug-toolbar`, `django-extensions`.
- Remove from base `INSTALLED_APPS`: `django_extensions`. Keep debug toolbar behind `DEBUG` and out of the prod image.

Remove unused pins:

| Package | Action |
|---|---|
| `djangorestframework` | Remove |
| `pycryptodome` | Remove |
| `django-localflavor` | Remove |
| `simplejson` | Replace with stdlib `json` in `get_lat_lng` |
| `common/imagegenerators.py` | Delete (imports `imagekit`, not installed) |
| `web/fabfile.py` | Archive; `scripts/deploy-prod.sh` replaced it |

### 10. Vendor Font Awesome

- `base_fidouche.html` loads Font Awesome 4.3 from maxcdn with no SRI. Vendor it like jQuery. Move `FACEBOOK_APP_ID` to env if still required.

### 11. Dead code

- Delete or archive `web/legacy/` (not in `INSTALLED_APPS`).
- Drop `AUTH_PROFILE_MODULE` and `USE_L10N`.
- Look up the behind-the-music album by slug instead of `pk=3`.

## Phase 4 — Remaining performance

Not another fidouche queryset pass. Global cost the last optimization did not cover.

### 12. Context processors

- `random_quote` uses `ORDER BY RAND()` and `list_years_with_gigs` runs `Show.objects.dates()` on every request, including login/404.
- Cache years for a day. Pick a featured quote in Python or cache the quote for a few minutes.

### 13. Past shows

- `shows.views.past_shows` materializes the full public history unless `?year=` is set. Default to the latest year. Add a query-budget test.

### 14. Geocoding

- `Venue.save` calls Google with `urllib` and no timeout; `except Exception: raise Exception` hides the real error.
- Skip unless address fields changed. `timeout=5`. Log and continue so admin saves still work.

### 15. Gunicorn

- Non-root `USER` in the Dockerfile. `gunicorn --workers 3 --timeout 30`. Move collectstatic/migrate out of a one-line `bash -c`.

### 16. Login surface

- Add password-reset views if prod email works. Rate-limit `/accounts/login/` and `/admin/login/` (nginx or django-axes).

## Phase 5 — Platform upgrades (own branch)

Do not mix with phases 1–4. An earlier 4.2 attempt (PR #40) and a reverted upgrade already exist.

| Component | Now | Target |
|---|---|---|
| Python | 3.8 (EOL) | 3.12 |
| Django | 4.0.10 (EOL) | 4.2, then 5.2 LTS |
| Prod DB | mysql:5.7 (EOL) | MariaDB 10.11+ or MySQL 8 |
| Dev DB | mariadb:10.6 (LTS ended Jul 2026) | 10.11+ |

- Keep the SQLite-in-memory test harness from `036feeb`.
- `USE_TZ = True` is its own change: aware datetimes, `timezone.now()`. Do not fold it into Django 5.

jQuery 1.10.2 (XSS CVEs below 3.5) can ride with this branch or a small follow-up after checking `fidouche.js` / dataTables / datetimepicker.

## Out of scope

- Re-doing fidouche/setter prefetch and query budgets
- Social widget behavior
- RequireJS (already removed)
- Live-site CVE scan (not run during the audit)
