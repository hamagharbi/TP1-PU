from datetime import datetime, timedelta

import pytest

from app.domain.creneau import Creneau
from app.domain.erreurs import CreneauInvalide


def h(heure: int, minute: int = 0) -> datetime:
    return datetime(2026, 10, 8, heure, minute)


def test_creneau_valide_expose_sa_duree():
    assert Creneau(h(10), h(12)).duree == timedelta(hours=2)


@pytest.mark.parametrize("debut, fin", [(h(12), h(10)), (h(10), h(10))])
def test_debut_doit_preceder_fin(debut, fin):
    with pytest.raises(CreneauInvalide):
        Creneau(debut, fin)


@pytest.mark.parametrize(
    "autre",
    [Creneau(h(11), h(13)), Creneau(h(9), h(11)), Creneau(h(10, 30), h(11)), Creneau(h(9), h(13))],
)
def test_chevauchements_detectes(autre):
    creneau = Creneau(h(10), h(12))
    assert creneau.chevauche(autre)
    assert autre.chevauche(creneau)


def test_creneaux_contigus_ne_se_chevauchent_pas():
    assert not Creneau(h(10), h(12)).chevauche(Creneau(h(12), h(13)))
    assert not Creneau(h(12), h(13)).chevauche(Creneau(h(10), h(12)))
