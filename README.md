# Location de vélos et trottinettes — TP1 Processus Unifié

Petit système de location (6 cas d'utilisation) développé selon le Processus Unifié.

## Documents

- [Vision et acteurs](docs/01-vision.md)
- [Cas d'utilisation et priorisation](docs/02-cas-utilisation.md)
- [Plan des itérations, phases et jalons](docs/03-plan-iterations.md)
- [Fiche UC2 Réserver un véhicule](docs/fiches/UC2-reserver-vehicule.md)
- Diagrammes UML : [cas d'utilisation](docs/uml/cas-utilisation.puml), [classes UC2](docs/uml/classes-uc2.puml), [séquence UC2](docs/uml/sequence-uc2.puml)
- [Checklist de revue croisée](docs/revue/checklist-revue-croisee.md)

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

## API

| Méthode | Route | Réponses |
|---|---|---|
| POST | `/reservations` `{client_id, vehicule_id, debut, fin}` | 201, 404, 409, 422 |
| GET | `/reservations/{id}` | 200, 404 |

Erreurs métier : `{"erreur": "<CODE>", "message": "..."}`. Montants en centimes (`montant_estime_centimes`).

## Limites connues

L'authentification est hors périmètre de ce TP : le `client_id` est fourni dans la requête et
`GET /reservations/{id}` n'est pas restreint au propriétaire. À traiter avant tout déploiement réel.

## Publier sur GitHub

```bash
git remote add origin <url>
bash github/setup-github.sh <owner>/<repo>   # milestones, tickets, project board, push branches + tags
```

## Jalons (tags)

| Tag | Phase |
|---|---|
| `v0.0-lancement` | Lancement terminé (LCO) |
| `v0.1-elaboration` | Architecture de base exécutable (LCA) |
