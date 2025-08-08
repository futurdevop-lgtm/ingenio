# Talent Platform (Django + DRF)

Requirements: Python 3.13, Redis (optional for Channels)

Quickstart

1) Create venv and install deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run migrations and dev server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

API
- Auth: `POST /api/accounts/auth/token/` (JWT)
- Users: `/api/accounts/users/` (register: `POST /api/accounts/users/register/`)
- Profiles: `/api/profiles/profiles/`, Skills `/api/profiles/skills/`, Certs `/api/profiles/certifications/`
- Projects: `/api/projects/` requirements inline; matching: `/api/projects/{id}/match/`
- Assignments: `/api/projects/assignments/`
- Search: `/api/search/engineers/` with filters: stack, level, domain, availability, location, skill (multi), min_years
- Dashboard: `/api/dashboard/manager/`
- Docs: `/api/docs/`

Notes
- Default permission: authenticated; use JWT.
- Media upload stored in `media/`.