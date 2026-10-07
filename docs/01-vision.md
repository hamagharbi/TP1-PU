# Vision — Location de vélos et trottinettes

## Vision (5 lignes)

1. **Problème** : louer un vélo ou une trottinette en station se fait sans garantie de disponibilité ; doubles réservations et manque de visibilité frustrent les usagers.
2. **Utilisateurs** : clients (étudiants, salariés, touristes) et opérateurs de flotte.
3. **Valeur client** : réserver en ligne un véhicule sur un créneau garanti sans conflit, payer et restituer simplement.
4. **Valeur opérateur** : visibilité sur la flotte, moins de litiges.
5. **Périmètre** : API web, stations fixes, paiement via une passerelle externe simulée.

## Acteurs

| Acteur | Type | Rôle |
|---|---|---|
| Client | principal | consulte, réserve, paie, annule, restitue |
| Opérateur de flotte | principal | gère les véhicules (ajout, retrait, maintenance) |
| Passerelle de paiement | secondaire (système externe) | autorise et capture les paiements |
