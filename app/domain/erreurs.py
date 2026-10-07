class ErreurMetier(Exception):
    """Erreur métier : porte un code stable et le statut HTTP associé."""

    code = "ERREUR_METIER"
    http_status = 400

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class CreneauInvalide(ErreurMetier):
    code = "CRENEAU_INVALIDE"
    http_status = 422


class ClientIntrouvable(ErreurMetier):
    code = "CLIENT_INTROUVABLE"
    http_status = 404


class VehiculeIntrouvable(ErreurMetier):
    code = "VEHICULE_INTROUVABLE"
    http_status = 404


class ConflitReservation(ErreurMetier):
    code = "CONFLIT_RESERVATION"
    http_status = 409


class CreneauDansLePasse(ErreurMetier):
    code = "CRENEAU_DANS_LE_PASSE"
    http_status = 422


class ReservationIntrouvable(ErreurMetier):
    code = "RESERVATION_INTROUVABLE"
    http_status = 404


class VehiculeIndisponible(ErreurMetier):
    code = "VEHICULE_INDISPONIBLE"
    http_status = 409


class ConflitClient(ErreurMetier):
    code = "CONFLIT_CLIENT"
    http_status = 409
