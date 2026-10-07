from datetime import datetime

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.enums import EtatVehicule, StatutReservation, TypeVehicule


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str]
    email: Mapped[str]


class Vehicule(Base):
    __tablename__ = "vehicules"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[TypeVehicule]
    station: Mapped[str]
    etat: Mapped[EtatVehicule] = mapped_column(default=EtatVehicule.DISPONIBLE)


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (Index("ix_reservations_vehicule_creneau", "vehicule_id", "debut", "fin"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    vehicule_id: Mapped[int] = mapped_column(ForeignKey("vehicules.id"))
    debut: Mapped[datetime]
    fin: Mapped[datetime]
    statut: Mapped[StatutReservation]
    montant_estime_centimes: Mapped[int]
