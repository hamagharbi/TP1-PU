# UC2 : Réserver un véhicule (Construction)

Closes #2

## Contenu
- Fiche UC : `docs/fiches/UC2-reserver-vehicule.md`
- Diagrammes : `docs/uml/classes-uc2.puml`, `docs/uml/sequence-uc2.puml`
- Métier : `Creneau` (durée max 24 h, UTC), tarif en centimes, erreurs métier
- Service : règles R1 à R6, `obtenir`
- Accès aux données : chevauchement véhicule/client, transaction `BEGIN IMMEDIATE`
- API : `POST /reservations`, `GET /reservations/{id}`

## Tests
- Unitaires : `Creneau`, tarif, `ReservationService` (faux dépôts, nominal + R1 à R6)
- Intégration : scénario nominal réserver → consulter, erreurs, fuseaux horaires
- Concurrence : 2 réservations simultanées → 1 succès, 1 conflit

## Revue croisée
Merci de remplir `docs/revue/checklist-revue-croisee.md`.
