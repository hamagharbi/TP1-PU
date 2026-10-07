import math
from datetime import timedelta

from app.domain.creneau import Creneau
from app.domain.enums import TypeVehicule

TARIF_HORAIRE_CENTIMES: dict[TypeVehicule, int] = {
    TypeVehicule.VELO: 200,
    TypeVehicule.TROTTINETTE: 300,
}


def montant_estime_centimes(type_vehicule: TypeVehicule, creneau: Creneau) -> int:
    """Toute heure entamée est due."""
    heures_entamees = math.ceil(creneau.duree / timedelta(hours=1))
    return heures_entamees * TARIF_HORAIRE_CENTIMES[type_vehicule]
