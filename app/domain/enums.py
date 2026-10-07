from enum import StrEnum


class TypeVehicule(StrEnum):
    VELO = "VELO"
    TROTTINETTE = "TROTTINETTE"


class EtatVehicule(StrEnum):
    DISPONIBLE = "DISPONIBLE"
    EN_MAINTENANCE = "EN_MAINTENANCE"


class StatutReservation(StrEnum):
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"
