# Fiche UC2 — Réserver un véhicule

| Rubrique | Contenu |
|---|---|
| Acteur principal | Client |
| Parties prenantes | Client (créneau garanti) ; Opérateur (pas de double réservation) |
| Niveau | objectif utilisateur |
| Préconditions | le client est identifié ; le véhicule existe |
| Garanties en cas de succès | une réservation `CONFIRMEE` est enregistrée avec son montant estimé ; aucune autre réservation confirmée ne chevauche ce créneau pour ce véhicule ni pour ce client |
| Garanties minimales | en cas d'échec, rien n'est enregistré |
| Déclencheur | le client choisit un véhicule (issu de UC1) et un créneau |

## Scénario nominal

1. Le client envoie sa demande : identifiant client, identifiant véhicule, début, fin.
2. Le système vérifie le créneau (début avant la fin, durée ≤ 24 h, début dans le futur).
3. Le système vérifie que le client et le véhicule existent.
4. Le système vérifie que le véhicule n'est pas en maintenance.
5. Le système vérifie qu'aucune réservation confirmée ne chevauche le créneau pour ce véhicule.
6. Le système vérifie que le client n'a pas déjà une réservation confirmée sur ce créneau.
7. Le système calcule le montant estimé (vélo 2 €/h, trottinette 3 €/h, heure entamée due).
8. Le système enregistre la réservation `CONFIRMEE` et la renvoie au client (HTTP 201).

## Scénarios alternatifs

- **2a** Début ≥ fin ou durée > 24 h → `CRENEAU_INVALIDE` (422).
- **2b** Début ≤ maintenant → `CRENEAU_DANS_LE_PASSE` (422).
- **3a** Client inconnu → `CLIENT_INTROUVABLE` (404) ; véhicule inconnu → `VEHICULE_INTROUVABLE` (404).
- **4a** Véhicule en maintenance → `VEHICULE_INDISPONIBLE` (409).
- **5a** Créneau déjà réservé pour ce véhicule → `CONFLIT_RESERVATION` (409).
- **6a** Le client a déjà une réservation qui chevauche → `CONFLIT_CLIENT` (409).

## Règles métier

| Règle | Énoncé |
|---|---|
| R1 | `debut < fin` et durée ≤ 24 h |
| R2 | `debut` strictement après l'instant courant |
| R3 | client et véhicule existent |
| R4 | véhicule non `EN_MAINTENANCE` |
| R5 | pas de chevauchement avec une réservation `CONFIRMEE` du véhicule |
| R6 | pas de chevauchement avec une réservation `CONFIRMEE` du client |

Chevauchement : `a.debut < b.fin et b.debut < a.fin` (créneaux contigus autorisés). Dates sans fuseau = UTC.

## Exigences non fonctionnelles

- **Concurrence** : deux demandes simultanées sur le même créneau → exactement une réussit (transaction `BEGIN IMMEDIATE`).
- Temps de réponse < 200 ms en charge nominale.

## Traçabilité

Ticket #2 · branche `uc2-reserver-vehicule` · classes `docs/uml/classes-uc2.puml` · séquence `docs/uml/sequence-uc2.puml` · tests `tests/unit/test_reservation_service.py`, `tests/integration/test_api_reservations.py`, `tests/integration/test_concurrence.py`.
