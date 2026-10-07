from collections.abc import Callable
from datetime import datetime

from app.domain.creneau import Creneau, maintenant_utc
from app.domain.enums import EtatVehicule, StatutReservation
from app.domain.erreurs import (
    ClientIntrouvable,
    ConflitClient,
    ConflitReservation,
    CreneauDansLePasse,
    ReservationIntrouvable,
    VehiculeIndisponible,
    VehiculeIntrouvable,
)
from app.domain.tarif import montant_estime_centimes
from app.models import Reservation
from app.services.ports import UniteDeTravail


class ReservationService:
    def __init__(self, uow: UniteDeTravail, horloge: Callable[[], datetime] = maintenant_utc) -> None:
        self._uow = uow
        self._horloge = horloge

    def reserver(self, client_id: int, vehicule_id: int, debut: datetime, fin: datetime) -> Reservation:
        creneau = Creneau(debut, fin)  # R1
        if creneau.debut <= self._horloge():  # R2
            raise CreneauDansLePasse("Le créneau doit commencer dans le futur.")
        with self._uow as uow:
            if uow.clients.obtenir(client_id) is None:  # R3
                raise ClientIntrouvable(f"Client {client_id} introuvable.")
            vehicule = uow.vehicules.obtenir(vehicule_id)
            if vehicule is None:  # R3
                raise VehiculeIntrouvable(f"Véhicule {vehicule_id} introuvable.")
            if vehicule.etat == EtatVehicule.EN_MAINTENANCE:  # R4
                raise VehiculeIndisponible("Le véhicule est en maintenance.")
            if uow.reservations.existe_chevauchement_vehicule(vehicule_id, creneau):  # R5
                raise ConflitReservation("Le véhicule est déjà réservé sur ce créneau.")
            if uow.reservations.existe_chevauchement_client(client_id, creneau):  # R6
                raise ConflitClient("Vous avez déjà une réservation sur ce créneau.")
            reservation = Reservation(
                client_id=client_id,
                vehicule_id=vehicule_id,
                debut=creneau.debut,
                fin=creneau.fin,
                statut=StatutReservation.CONFIRMEE,
                montant_estime_centimes=montant_estime_centimes(vehicule.type, creneau),
            )
            uow.reservations.ajouter(reservation)
            uow.valider()
            return reservation

    def obtenir(self, reservation_id: int) -> Reservation:
        with self._uow as uow:
            reservation = uow.reservations.obtenir(reservation_id)
            if reservation is None:
                raise ReservationIntrouvable(f"Réservation {reservation_id} introuvable.")
            return reservation
