from datetime import datetime, timedelta

import pytest

from app.domain.creneau import Creneau
from app.domain.enums import TypeVehicule
from app.domain.tarif import montant_estime_centimes

DEBUT = datetime(2026, 10, 8, 10, 0)


@pytest.mark.parametrize(
    "type_vehicule, duree, attendu",
    [
        (TypeVehicule.VELO, timedelta(hours=1), 200),
        (TypeVehicule.VELO, timedelta(hours=2), 400),
        (TypeVehicule.TROTTINETTE, timedelta(minutes=90), 600),
        (TypeVehicule.VELO, timedelta(minutes=1), 200),
        (TypeVehicule.VELO, timedelta(hours=1, microseconds=1), 400),
        (TypeVehicule.TROTTINETTE, timedelta(hours=24), 7200),
    ],
)
def test_heure_entamee_due(type_vehicule, duree, attendu):
    assert montant_estime_centimes(type_vehicule, Creneau(DEBUT, DEBUT + duree)) == attendu
