# Cas d'utilisation et priorisation

## Liste des UC

| # | Cas d'utilisation | Acteur(s) | Description courte |
|---|---|---|---|
| UC1 | Consulter les véhicules disponibles | Client | lister les véhicules libres d'une station sur un créneau |
| UC2 | Réserver un véhicule | Client | bloquer un véhicule sur un créneau — **UC à risque technique : conflits de réservation** |
| UC3 | Payer la location | Client, Passerelle de paiement | régler le montant via la passerelle externe |
| UC4 | Annuler une réservation | Client | libérer un créneau réservé |
| UC5 | Restituer le véhicule | Client | clore la location, calculer le prix final (inclut UC3) |
| UC6 | Gérer la flotte | Opérateur de flotte | ajouter, retirer, mettre en maintenance un véhicule |

Diagramme : [`uml/cas-utilisation.puml`](uml/cas-utilisation.puml).

## Priorisation

Notes de 1 (faible) à 3 (fort).

| UC | Valeur métier | Risque | Impact architecture | Total | Itération |
|---|---|---|---|---|---|
| UC2 Réserver un véhicule | 3 | 3 | 3 | **9** | It1 (Élaboration) |
| UC3 Payer la location | 3 | 3 | 2 | 8 | It2 |
| UC1 Consulter les disponibilités | 3 | 1 | 2 | 6 | It1 |
| UC5 Restituer le véhicule | 2 | 2 | 2 | 6 | It2 |
| UC6 Gérer la flotte | 2 | 1 | 2 | 5 | It3 |
| UC4 Annuler une réservation | 2 | 1 | 1 | 4 | It3 |

**À traiter en premier : UC2** (score maximal sur les trois critères : il fixe le modèle de données, la
gestion transactionnelle et la stratégie anti-conflit), puis **UC3** (intégration externe risquée).
