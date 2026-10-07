# Plan des itérations, phases et jalons (Processus Unifié)

| Phase | Itération | Contenu | Jalon | Tag |
|---|---|---|---|---|
| Lancement | — (cadrage) | vision, acteurs, UC, priorisation, plan | LCO — Objectifs du cycle de vie | `v0.0-lancement` |
| Élaboration | It1 | architecture de base exécutable : `POST /reservations` de bout en bout (UC2), CI verte ; UC1 en lecture | LCA — Architecture du cycle de vie | `v0.1-elaboration` |
| Construction | It2 | UC2 complet (règles, alternatives, concurrence), UC3, UC5 | — | — |
| Construction | It3 | UC4, UC6 | IOC — Capacité opérationnelle initiale | `v0.2-construction` |
| Transition | fin It3 | revue croisée, recette, documentation de déploiement | PR — Livraison du produit | `v1.0-transition` |

## Itérations

- **It1 (Élaboration)** — objectif : lever le risque technique. Livrable : route bout-en-bout contrôleur → service → accès aux données pour UC2, premier test automatisé en CI.
- **It2 (Construction)** — UC2 complet (fiche, classes, séquence, tests unitaires + intégration), UC3, UC5.
- **It3 (Construction → Transition)** — UC4, UC6, revue croisée, stabilisation, livraison.

## Correspondance GitHub

- Milestones = phases : `Lancement`, `Élaboration`, `Construction`, `Transition`.
- Tickets = UC (UC1…UC6) + un ticket par livrable de phase.
- Une branche par UC ; jalons de phase = tags Git.
