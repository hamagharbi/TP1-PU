# Spec — Location de vélos/trottinettes (TP1 Processus Unifié)

Date : 2026-10-07 · Statut : validé en brainstorming

## 1. Contexte et objectifs

TP1 « Processus unifié et approches agiles ». Livrer, dans un dépôt Git :

- le cadrage (vision, acteurs, UC, priorisation, plan d'itérations/phases/jalons) ;
- **Partie 1 – Élaboration** : dépôt, tickets/milestones (préparés localement), diagramme de cas
  d'utilisation PlantUML, architecture de base exécutable pour l'UC à risque avec un test en CI,
  tag `v0.1-elaboration` ;
- **Partie 2 – Construction** : UC2 complet (fiche UC → classes + séquence PlantUML → code en couches →
  tests unitaires + intégration), support de revue croisée.

Stack : **Python 3.13, FastAPI, SQLAlchemy 2, SQLite, pytest, GitHub Actions**.

Contraintes : tout en local ; le remote GitHub sera fourni plus tard par l'utilisateur. `gh` n'est pas
installé : tickets/milestones/project board sont préparés en fichiers + script `gh`.

### Critères de réussite

1. `v0.1-elaboration` pointe sur un commit où `POST /reservations` traverse contrôleur → service → dépôt
   SQLite, et où `pytest` passe (≥ 1 test d'intégration).
2. UC2 complet : fiche UC, diagrammes de classes et de séquence, règles R1–R6, tests unitaires, test
   d'intégration du scénario nominal et test de concurrence, tous verts.
3. Chaque UC a une branche ; les jalons de phase sont des tags.

## 2. Cadrage

### 2.1 Vision (5 lignes)

1. **Problème** : louer un vélo ou une trottinette en station se fait sans garantie de disponibilité ;
   doubles réservations et manque de visibilité frustrent les usagers.
2. **Utilisateurs** : clients (étudiants, salariés, touristes) et opérateurs de flotte.
3. **Valeur client** : réserver en ligne un véhicule sur un créneau garanti sans conflit, payer et
   restituer simplement.
4. **Valeur opérateur** : visibilité sur la flotte, moins de litiges.
5. **Périmètre** : API web, stations fixes, paiement via passerelle externe simulée.

### 2.2 Acteurs

| Acteur | Type | Rôle |
|---|---|---|
| Client | principal | consulte, réserve, paie, annule, restitue |
| Opérateur de flotte | principal | gère les véhicules (ajout, retrait, maintenance) |
| Passerelle de paiement | secondaire (système externe) | autorise/capture les paiements |

### 2.3 Cas d'utilisation

| # | UC | Acteur(s) |
|---|---|---|
| UC1 | Consulter les véhicules disponibles | Client |
| UC2 | Réserver un véhicule (**à risque : conflit de réservation**) | Client |
| UC3 | Payer la location | Client, Passerelle de paiement |
| UC4 | Annuler une réservation | Client |
| UC5 | Restituer le véhicule | Client |
| UC6 | Gérer la flotte | Opérateur de flotte |

### 2.4 Priorisation (1 à 3 ; V = valeur métier, R = risque, A = impact architecture)

| UC | V | R | A | Total | Itération |
|---|---|---|---|---|---|
| UC2 Réserver | 3 | 3 | 3 | 9 | It1 |
| UC3 Payer | 3 | 3 | 2 | 8 | It2 |
| UC1 Consulter | 3 | 1 | 2 | 6 | It1 |
| UC5 Restituer | 2 | 2 | 2 | 6 | It2 |
| UC6 Gérer flotte | 2 | 1 | 2 | 5 | It3 |
| UC4 Annuler | 2 | 1 | 1 | 4 | It3 |

À traiter en premier : **UC2**, puis UC3.

### 2.5 Phases, itérations, jalons

| Phase | Itération | Contenu | Jalon → tag |
|---|---|---|---|
| Lancement | — (cadrage) | vision, acteurs, UC, priorisation, plan | LCO → `v0.0-lancement` |
| Élaboration | It1 | architecture de base exécutable UC2, CI verte | LCA → `v0.1-elaboration` |
| Construction | It2, It3 | UC2 complet (ce TP), puis UC3, UC1, UC5, UC4, UC6 | IOC → `v0.2-construction` |
| Transition | fin It3 | revue croisée, recette, doc de déploiement | PR → `v1.0-transition` |

Livré dans ce TP : tags `v0.0-lancement`, `v0.1-elaboration` ; milestones Lancement et Élaboration
marqués fermés ; UC2 complet fusionné. Milestones Construction/Transition restent ouverts.

## 3. Organisation du dépôt

```
docs/01-vision.md, 02-cas-utilisation.md, 03-plan-iterations.md
docs/fiches/UC2-reserver-vehicule.md
docs/uml/cas-utilisation.puml, classes-uc2.puml, sequence-uc2.puml
docs/revue/checklist-revue-croisee.md
github/issues/UC1..UC6.md, github/milestones.md, github/setup-github.sh
app/ (code), tests/, .github/workflows/ci.yml, requirements.txt, pyproject.toml, README.md
```

### Flux Git

1. `main` : cadrage + UML cas d'utilisation + `github/` → tag `v0.0-lancement`.
2. Branche `uc2-reserver-vehicule` : squelette bout-en-bout + test + CI → merge `--no-ff` dans `main`
   (message « Closes #2 ») → tag `v0.1-elaboration`.
3. Même branche : fiche UC, classes, séquence, code complet, tests → merge dans `main`.
4. Branches créées pour les autres UC : `uc1-consulter-disponibilites`, `uc3-payer-location`,
   `uc4-annuler-reservation`, `uc5-restituer-vehicule`, `uc6-gerer-flotte`.
5. Au remote fourni : `git push --all && git push --tags` puis `github/setup-github.sh`.

## 4. Architecture

| Couche | Emplacement | Rôle |
|---|---|---|
| Contrôleur | `app/api/reservations.py` | routeur FastAPI, schémas Pydantic, HTTP ↔ service |
| Métier | `app/domain/creneau.py`, `tarif.py`, `erreurs.py` | objets purs : `Creneau`, calcul de montant, exceptions |
| Service | `app/services/reservation_service.py` | orchestration UC2, règles, transaction ; dépend de `Protocol` + horloge injectable |
| Accès aux données | `app/repositories/`, `app/db.py`, `app/models.py` | modèles et dépôts SQLAlchemy, SQLite |

### 4.1 Modèle de données

- `Client(id, nom, email)`
- `Vehicule(id, type: VELO|TROTTINETTE, station, etat: DISPONIBLE|EN_MAINTENANCE)`
- `Reservation(id, client_id, vehicule_id, debut, fin, statut: CONFIRMEE|ANNULEE, montant_estime)`

Données de démonstration via `python -m app.seed`.

### 4.2 Routes

- `POST /reservations` `{client_id, vehicule_id, debut, fin}` → 201 + réservation
- `GET /reservations/{id}` → 200 | 404

### 4.3 Règles UC2 (version Construction)

| Règle | Description | Erreur | HTTP |
|---|---|---|---|
| R1 | `debut < fin` et durée ≤ 24 h | `CreneauInvalide` | 422 |
| R2 | `debut` strictement dans le futur (horloge injectée) | `CreneauDansLePasse` | 422 |
| R3 | client et véhicule existent | `ClientIntrouvable` / `VehiculeIntrouvable` | 404 |
| R4 | véhicule non `EN_MAINTENANCE` | `VehiculeIndisponible` | 409 |
| R5 | aucune réservation `CONFIRMEE` du véhicule ne chevauche le créneau | `ConflitReservation` | 409 |
| R6 | le client n'a pas déjà une réservation `CONFIRMEE` qui chevauche | `ConflitClient` | 409 |

Chevauchement : `a.debut < b.fin and b.debut < a.fin` (créneaux contigus = pas de conflit).

Montant estimé : vélo 2 €/h, trottinette 3 €/h, heure entamée due (`ceil(durée / 1 h) * tarif`).

### 4.4 Concurrence (risque technique)

Le service exécute vérifications R5/R6 + insertion dans une seule transaction démarrée par
`BEGIN IMMEDIATE` (verrou d'écriture SQLite). Deux demandes concurrentes sur le même créneau sont
sérialisées : la seconde voit la première réservation et lève `ConflitReservation`.
Engine configuré avec `isolation_level=None` côté pysqlite + événement `begin` émettant
`BEGIN IMMEDIATE`, et `timeout` de connexion pour attendre le verrou.

### 4.5 Erreurs

Toutes les erreurs métier héritent de `ErreurMetier(code, message, http_status)`. Un gestionnaire
d'exceptions FastAPI renvoie `{"erreur": code, "message": message}` avec le statut associé.

## 5. Élaboration — périmètre minimal

`POST /reservations` avec R3 et R5 uniquement (+ R1 minimal `debut < fin` porté par `Creneau`).
Test d'intégration : créneau libre → 201, même créneau → 409. CI GitHub Actions verte.

## 6. Construction — tests

- **Unitaires** : `Creneau` (validation, chevauchement, contigus), tarif, `ReservationService` avec
  faux dépôts en mémoire (nominal + R1…R6).
- **Intégration (scénario nominal)** : `TestClient` + SQLite fichier temporaire : réservation → 201 avec
  montant → `GET` renvoie la même réservation.
- **Concurrence** : 2 threads, même créneau, exactement 1 succès et 1 `ConflitReservation`.

## 7. Revue croisée

Non réalisable par l'agent : fourniture de `docs/revue/checklist-revue-croisee.md` et d'une
description de PR pour l'équipe relectrice.

## 8. Hors périmètre

UC1, UC3–UC6 (tickets + branches seulement), authentification, front-end, déploiement réel.
