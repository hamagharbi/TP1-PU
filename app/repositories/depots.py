from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.creneau import Creneau
from app.domain.enums import StatutReservation
from app.models import Client, Reservation, Vehicule


class SqlClientRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def obtenir(self, client_id: int) -> Client | None:
        return self._session.get(Client, client_id)


class SqlVehiculeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def obtenir(self, vehicule_id: int) -> Vehicule | None:
        return self._session.get(Vehicule, vehicule_id)


class SqlReservationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def ajouter(self, reservation: Reservation) -> Reservation:
        self._session.add(reservation)
        self._session.flush()
        return reservation

    def obtenir(self, reservation_id: int) -> Reservation | None:
        return self._session.get(Reservation, reservation_id)

    def existe_chevauchement_vehicule(self, vehicule_id: int, creneau: Creneau) -> bool:
        return self._existe_chevauchement(Reservation.vehicule_id == vehicule_id, creneau)

    def existe_chevauchement_client(self, client_id: int, creneau: Creneau) -> bool:
        return self._existe_chevauchement(Reservation.client_id == client_id, creneau)

    def _existe_chevauchement(self, critere, creneau: Creneau) -> bool:
        requete = (
            select(Reservation.id)
            .where(
                critere,
                Reservation.statut == StatutReservation.CONFIRMEE,
                Reservation.debut < creneau.fin,
                Reservation.fin > creneau.debut,
            )
            .limit(1)
        )
        return self._session.scalar(requete) is not None
