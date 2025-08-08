# Plateforme de Talents (Django + DRF)

Prérequis: Python 3.13, Redis (optionnel pour Channels)

Démarrage rapide

1) Créer l'environnement virtuel et installer les dépendances

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Lancer les migrations et le serveur de dev

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

API
- Auth: `POST /api/comptes/auth/jeton/` (JWT)
- Utilisateurs: `/api/comptes/utilisateurs/` (inscription: `POST /api/comptes/utilisateurs/inscription/`)
- Profils ingénieurs: `/api/profils/ingenieurs/`, Compétences `/api/profils/competences/`, Certifications `/api/profils/certifications/`
- Projets: `/api/projets/` exigences inline; matching: `/api/projets/{id}/matching/`
- Affectations: `/api/projets/affectations/`
- Recherche: `/api/recherche/ingenieurs/?pile=MEAN&niveau=Senior&disponibilite=remote&localisation=Paris&competence=AWS&competence=Docker&min_annees=3`
- Tableau de bord: `/api/tableau/manager/`
- Docs: `/api/docs/`

Notes
- Permission par défaut: authentifié; utilisez JWT.
- Les CV sont stockés dans `media/`.