from datetime import datetime

import pytest

from app.domain.enums import EtatVehicule, StatutReservation, TypeVehicule
from app.domain.erreurs import (
    ClientIntrouvable,
    ConflitClient,
    ConflitReservation,
    CreneauDansLePasse,
    CreneauInvalide,
    ReservationIntrouvable,
    VehiculeIndisponible,
    VehiculeIntrouvable,
)
from app.models import Client, Reservation, Vehicule
from app.services.reservation_service import ReservationService
from tests.constantes import MAINTENANT
from tests.fakes import FausseUniteDeTravail

VELO, TROTTINETTE, EN_PANNE = 1, 2, 3
ALICE, BOB = 1, 2


def h(heure: int, minute: int = 0) -> datetime:
    return datetime(2026, 10, 8, heure, minute)


@pytest.fixture
def uow():
    return FausseUniteDeTravail(
        clients=[Client(id=ALICE, nom="Alice", email="a@x.fr"), Client(id=BOB, nom="Bob", email="b@x.fr")],
        vehicules=[
            Vehicule(id=VELO, type=TypeVehicule.VELO, station="Gare", etat=EtatVehicule.DISPONIBLE),
            Vehicule(id=TROTTINETTE, type=TypeVehicule.TROTTINETTE, station="Campus", etat=EtatVehicule.DISPONIBLE),
            Vehicule(id=EN_PANNE, type=TypeVehicule.VELO, station="Gare", etat=EtatVehicule.EN_MAINTENANCE),
        ],
    )


@pytest.fixture
def service(uow):
    return ReservationService(uow, horloge=lambda: MAINTENANT)


def test_scenario_nominal_enregistre_une_reservation_confirmee(service, uow):
    reservation = service.reserver(ALICE, TROTTINETTE, h(10), h(11, 30))

    assert reservation.id == 1
    assert reservation.statut == StatutReservation.CONFIRMEE
    assert reservation.montant_estime_centimes == 600
    assert uow.reservations.elements == [reservation]
    assert uow.valide


def test_r1_creneau_invalide(service, uow):
    with pytest.raises(CreneauInvalide):
        service.reserver(ALICE, VELO, h(12), h(10))
    assert not uow.valide


def test_r2_creneau_dans_le_passe(service):
    with pytest.raises(CreneauDansLePasse):
        service.reserver(ALICE, VELO, datetime(2026, 10, 7, 7, 0), datetime(2026, 10, 7, 9, 0))


def test_r2_debut_egal_a_maintenant_refuse(service):
    with pytest.raises(CreneauDansLePasse):
        service.reserver(ALICE, VELO, MAINTENANT, datetime(2026, 10, 7, 9, 0))


def test_r3_client_introuvable(service):
    with pytest.raises(ClientIntrouvable):
        service.reserver(99, VELO, h(10), h(11))


def test_r3_vehicule_introuvable(service):
    with pytest.raises(VehiculeIntrouvable):
        service.reserver(ALICE, 99, h(10), h(11))


def test_r4_vehicule_en_maintenance(service, uow):
    with pytest.raises(VehiculeIndisponible):
        service.reserver(ALICE, EN_PANNE, h(10), h(11))
    assert uow.reservations.elements == []


def test_r5_conflit_sur_le_vehicule(service, uow):
    service.reserver(ALICE, VELO, h(10), h(12))
    uow.valide = False
    with pytest.raises(ConflitReservation):
        service.reserver(BOB, VELO, h(11), h(13))
    assert not uow.valide
    assert len(uow.reservations.elements) == 1


def test_r5_creneau_contigu_accepte(service):
    service.reserver(ALICE, VELO, h(10), h(12))
    assert service.reserver(BOB, VELO, h(12), h(13)).id == 2


def test_reservation_annulee_ne_bloque_pas(service, uow):
    uow.reservations.ajouter(
        Reservation(
            client_id=BOB, vehicule_id=VELO, debut=h(10), fin=h(12),
            statut=StatutReservation.ANNULEE, montant_estime_centimes=400,
        )
    )
    assert service.reserver(ALICE, VELO, h(10), h(12)).statut == StatutReservation.CONFIRMEE


def test_r6_conflit_pour_le_client(service):
    service.reserver(ALICE, VELO, h(10), h(12))
    with pytest.raises(ConflitClient):
        service.reserver(ALICE, TROTTINETTE, h(11), h(13))


def test_obtenir_reservation_existante(service):
    reservation = service.reserver(ALICE, VELO, h(10), h(11))
    assert service.obtenir(reservation.id) is reservation


def test_obtenir_reservation_introuvable(service):
    with pytest.raises(ReservationIntrouvable):
        service.obtenir(42)
