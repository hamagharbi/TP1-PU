from typing import Self

from app.domain.creneau import Creneau
from app.domain.enums import StatutReservation
from app.models import Client, Reservation, Vehicule


class FauxDepotParId:
    def __init__(self, elements) -> None:
        self._par_id = {e.id: e for e in elements}

    def obtenir(self, identifiant: int):
        return self._par_id.get(identifiant)


class FauxDepotReservations:
    def __init__(self) -> None:
        self.elements: list[Reservation] = []

    def ajouter(self, reservation: Reservation) -> Reservation:
        reservation.id = len(self.elements) + 1
        self.elements.append(reservation)
        return reservation

    def obtenir(self, reservation_id: int) -> Reservation | None:
        return next((r for r in self.elements if r.id == reservation_id), None)

    def _confirmees_qui_chevauchent(self, creneau: Creneau):
        return (
            r
            for r in self.elements
            if r.statut == StatutReservation.CONFIRMEE and Creneau(r.debut, r.fin).chevauche(creneau)
        )

    def existe_chevauchement_vehicule(self, vehicule_id: int, creneau: Creneau) -> bool:
        return any(r.vehicule_id == vehicule_id for r in self._confirmees_qui_chevauchent(creneau))

    def existe_chevauchement_client(self, client_id: int, creneau: Creneau) -> bool:
        return any(r.client_id == client_id for r in self._confirmees_qui_chevauchent(creneau))


class FausseUniteDeTravail:
    def __init__(self, clients: list[Client], vehicules: list[Vehicule]) -> None:
        self.clients = FauxDepotParId(clients)
        self.vehicules = FauxDepotParId(vehicules)
        self.reservations = FauxDepotReservations()
        self.valide = False

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def valider(self) -> None:
        self.valide = True
