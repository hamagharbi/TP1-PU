from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.domain.enums import StatutReservation
from app.repositories.unite_de_travail import SqlUniteDeTravail
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["Réservations"])

ID_MAX = 2**63 - 1  # plus grand entier stockable par SQLite
Identifiant = Annotated[int, Field(ge=1, le=ID_MAX)]


class DemandeReservation(BaseModel):
    client_id: Identifiant
    vehicule_id: Identifiant
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
    montant_estime_centimes: int

    @field_serializer("debut", "fin")
    def _en_utc_explicite(self, moment: datetime) -> datetime:
        # Les dates sont stockées en UTC sans fuseau : on le rend explicite (suffixe Z).
        return moment.replace(tzinfo=timezone.utc)


def service_reservation(request: Request) -> ReservationService:
    return ReservationService(
        SqlUniteDeTravail(request.app.state.fabrique_sessions), horloge=request.app.state.horloge
    )


@router.post("", status_code=201, response_model=ReservationLue)
def reserver(
    demande: DemandeReservation, service: ReservationService = Depends(service_reservation)
):
    return service.reserver(demande.client_id, demande.vehicule_id, demande.debut, demande.fin)


@router.get("/{reservation_id}", response_model=ReservationLue)
def obtenir(
    reservation_id: Annotated[int, Path(ge=1, le=ID_MAX)],
    service: ReservationService = Depends(service_reservation),
):
    return service.obtenir(reservation_id)
