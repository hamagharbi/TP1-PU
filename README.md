# Location de vélos et trottinettes — TP1 Processus Unifié

Petit système de location (6 cas d'utilisation) développé selon le Processus Unifié.

## Documents

- [Vision et acteurs](docs/01-vision.md)
- [Cas d'utilisation et priorisation](docs/02-cas-utilisation.md)
- [Plan des itérations, phases et jalons](docs/03-plan-iterations.md)

## Lancer l'application

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # Linux/macOS : .venv/bin/python
.venv/Scripts/python -m app.seed                           # données de démonstration
.venv/Scripts/python -m uvicorn app.main:creer_app --factory --reload
```

Documentation interactive : http://127.0.0.1:8000/docs

## Tests

```bash
.venv/Scripts/python -m pytest -v
```

## Architecture

`app/api` (contrôleur) → `app/services` (service UC) → `app/repositories` (accès aux données, SQLite) ;
`app/domain` contient le métier pur (créneau, erreurs).

## Jalons (tags)

| Tag | Phase |
|---|---|
| `v0.0-lancement` | Lancement terminé (LCO) |
| `v0.1-elaboration` | Architecture de base exécutable (LCA) |
