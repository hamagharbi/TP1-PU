from datetime import datetime

import pytest

from app.db import creer_engine, creer_fabrique_sessions, initialiser_schema
from app.domain.creneau import Creneau
from app.domain.enums import StatutReservation, TypeVehicule
from app.models import Client, Reservation, Vehicule
from app.repositories.depots import (
    SqlClientRepository,
    SqlReservationRepository,
    SqlVehiculeRepository,
)


def h(heure: int) -> datetime:
    return datetime(2026, 10, 8, heure, 0)


@pytest.fixture
def session(tmp_path):
    engine = creer_engine(f"sqlite:///{tmp_path / 'test.db'}")
    initialiser_schema(engine)
    fabrique = creer_fabrique_sessions(engine)
    with fabrique() as session, session.begin():
        session.add_all(
            [
                Client(id=1, nom="Alice", email="alice@exemple.fr"),
                Vehicule(id=1, type=TypeVehicule.VELO, station="Gare"),
            ]
        )
        session.flush()
        yield session
    engine.dispose()


def _reservation(statut: StatutReservation) -> Reservation:
    return Reservation(client_id=1, vehicule_id=1, debut=h(10), fin=h(12), statut=statut)


def test_obtenir_client_et_vehicule(session):
    assert SqlClientRepository(session).obtenir(1).nom == "Alice"
    assert SqlVehiculeRepository(session).obtenir(1).type == TypeVehicule.VELO
    assert SqlVehiculeRepository(session).obtenir(99) is None


def test_ajouter_puis_obtenir_reservation(session):
    depot = SqlReservationRepository(session)
    ajoutee = depot.ajouter(_reservation(StatutReservation.CONFIRMEE))
    assert ajoutee.id is not None
    assert depot.obtenir(ajoutee.id).debut == h(10)


def test_detecte_chevauchement_avec_reservation_confirmee(session):
    depot = SqlReservationRepository(session)
    depot.ajouter(_reservation(StatutReservation.CONFIRMEE))
    assert depot.existe_chevauchement_vehicule(1, Creneau(h(11), h(13)))
    assert not depot.existe_chevauchement_vehicule(1, Creneau(h(12), h(13)))
    assert not depot.existe_chevauchement_vehicule(2, Creneau(h(11), h(13)))


def test_ignore_reservation_annulee(session):
    depot = SqlReservationRepository(session)
    depot.ajouter(_reservation(StatutReservation.ANNULEE))
    assert not depot.existe_chevauchement_vehicule(1, Creneau(h(10), h(12)))
