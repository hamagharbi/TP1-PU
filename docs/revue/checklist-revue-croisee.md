# Checklist de revue croisée — UC2 Réserver un véhicule

Équipe relectrice : ……………… · Date : ……………… · Commit relu : ………………

## Traçabilité UC → ticket → branche → classes → tests
- [ ] La fiche `docs/fiches/UC2-reserver-vehicule.md` couvre scénario nominal, alternatives 2a–6a, règles R1–R6.
- [ ] Chaque règle R1–R6 a au moins un test (`tests/unit/test_reservation_service.py`).
- [ ] Le diagramme de classes correspond aux classes du code (noms, méthodes, dépendances).
- [ ] Le diagramme de séquence correspond à `ReservationService.reserver`.

## Architecture en couches
- [ ] Le contrôleur (`app/api`) ne contient aucune règle métier.
- [ ] Le service ne dépend que d'interfaces (`app/services/ports.py`), pas de SQLAlchemy.
- [ ] Le domaine (`app/domain`) n'importe ni FastAPI ni SQLAlchemy.

## Risque technique : conflits
- [ ] La vérification du chevauchement et l'insertion sont dans la même transaction.
- [ ] `BEGIN IMMEDIATE` est en place (`app/db.py`) et le test de concurrence passe.
- [ ] Les créneaux contigus et les réservations annulées sont correctement gérés.

## Qualité
- [ ] `pytest -v` passe en local et en CI.
- [ ] Messages d'erreur clairs, codes HTTP cohérents (404 / 409 / 422).
- [ ] Nommage cohérent et lisible.

## Remarques
| # | Fichier:ligne | Remarque | Gravité | Réponse de l'équipe |
|---|---|---|---|---|
| 1 | | | | |
