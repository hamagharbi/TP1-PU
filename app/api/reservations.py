from datetime import datetime

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict

from app.domain.enums import StatutReservation
from app.repositories.unite_de_travail import SqlUniteDeTravail
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["Réservations"])


class DemandeReservation(BaseModel):
    client_id: int
    vehicule_id: int
    debut: datetime
    fin: datetime


class ReservationLue(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    vehicule_id: int
    debut: datetime
    fin: datetime
    statut: StatutReservation


def service_reservation(request: Request) -> ReservationService:
    return ReservationService(SqlUniteDeTravail(request.app.state.fabrique_sessions))


@router.post("", status_code=201, response_model=ReservationLue)
def reserver(
    demande: DemandeReservation, service: ReservationService = Depends(service_reservation)
):
    return service.reserver(demande.client_id, demande.vehicule_id, demande.debut, demande.fin)
