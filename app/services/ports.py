from typing import Protocol, Self

from app.domain.creneau import Creneau
from app.models import Client, Reservation, Vehicule


class ClientRepository(Protocol):
    def obtenir(self, client_id: int) -> Client | None: ...


class VehiculeRepository(Protocol):
    def obtenir(self, vehicule_id: int) -> Vehicule | None: ...


class ReservationRepository(Protocol):
    def ajouter(self, reservation: Reservation) -> Reservation: ...

    def obtenir(self, reservation_id: int) -> Reservation | None: ...

    def existe_chevauchement_vehicule(self, vehicule_id: int, creneau: Creneau) -> bool: ...

    def existe_chevauchement_client(self, client_id: int, creneau: Creneau) -> bool: ...


class UniteDeTravail(Protocol):
    clients: ClientRepository
    vehicules: VehiculeRepository
    reservations: ReservationRepository

    def __enter__(self) -> Self: ...

    def __exit__(self, *exc: object) -> None: ...

    def valider(self) -> None: ...
