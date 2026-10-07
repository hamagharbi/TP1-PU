from datetime import datetime

from app.domain.creneau import Creneau
from app.domain.enums import StatutReservation
from app.domain.erreurs import ClientIntrouvable, ConflitReservation, VehiculeIntrouvable
from app.models import Reservation
from app.services.ports import UniteDeTravail


class ReservationService:
    def __init__(self, uow: UniteDeTravail) -> None:
        self._uow = uow

    def reserver(self, client_id: int, vehicule_id: int, debut: datetime, fin: datetime) -> Reservation:
        creneau = Creneau(debut, fin)
        with self._uow as uow:
            if uow.clients.obtenir(client_id) is None:
                raise ClientIntrouvable(f"Client {client_id} introuvable.")
            if uow.vehicules.obtenir(vehicule_id) is None:
                raise VehiculeIntrouvable(f"Véhicule {vehicule_id} introuvable.")
            if uow.reservations.existe_chevauchement_vehicule(vehicule_id, creneau):
                raise ConflitReservation("Le véhicule est déjà réservé sur ce créneau.")
            reservation = Reservation(
                client_id=client_id,
                vehicule_id=vehicule_id,
                debut=creneau.debut,
                fin=creneau.fin,
                statut=StatutReservation.CONFIRMEE,
            )
            uow.reservations.ajouter(reservation)
            uow.valider()
            return reservation
