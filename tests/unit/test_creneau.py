from datetime import datetime, timedelta, timezone

import pytest

from app.domain.creneau import DUREE_MAX, Creneau, en_utc_naif
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


def test_duree_maximale_de_24h_acceptee():
    assert Creneau(h(0), h(0) + DUREE_MAX).duree == timedelta(hours=24)


def test_duree_superieure_a_24h_refusee():
    with pytest.raises(CreneauInvalide):
        Creneau(h(0), h(0) + DUREE_MAX + timedelta(seconds=1))


def test_normalise_en_utc_naif():
    paris = timezone(timedelta(hours=2))
    creneau = Creneau(datetime(2026, 10, 8, 10, 0, tzinfo=paris), h(9))
    assert creneau.debut == h(8)
    assert creneau.debut.tzinfo is None
    assert en_utc_naif(h(8)) == h(8)
