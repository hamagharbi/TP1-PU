import os

from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from app.db import creer_engine, creer_fabrique_sessions, initialiser_schema
from app.domain.enums import EtatVehicule, TypeVehicule
from app.models import Client, Vehicule


def peupler(fabrique_sessions: sessionmaker[Session]) -> None:
    """Insère les données de démonstration si la base est vide."""
    with fabrique_sessions() as session, session.begin():
        if session.scalar(select(func.count()).select_from(Client)):
            return
        session.add_all(
            [
                Client(id=1, nom="Alice", email="alice@exemple.fr"),
                Client(id=2, nom="Bob", email="bob@exemple.fr"),
                Vehicule(id=1, type=TypeVehicule.VELO, station="Gare"),
                Vehicule(id=2, type=TypeVehicule.TROTTINETTE, station="Campus"),
                Vehicule(id=3, type=TypeVehicule.VELO, station="Gare", etat=EtatVehicule.EN_MAINTENANCE),
            ]
        )


if __name__ == "__main__":
    engine = creer_engine(os.environ.get("DATABASE_URL", "sqlite:///./location.db"))
    initialiser_schema(engine)
    peupler(creer_fabrique_sessions(engine))
    print("Données de démonstration insérées.")
