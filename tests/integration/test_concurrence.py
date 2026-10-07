import threading
from datetime import datetime

from app.domain.erreurs import ConflitReservation
from app.repositories.unite_de_travail import SqlUniteDeTravail
from app.services.reservation_service import ReservationService
from tests.constantes import MAINTENANT


def test_deux_reservations_simultanees_un_seul_succes(app):
    fabrique = app.state.fabrique_sessions
    for jour in range(9, 19):  # 10 essais pour provoquer réellement la course
        barriere = threading.Barrier(2)
        resultats: list[str] = []

        def tenter(client_id: int) -> None:
            service = ReservationService(SqlUniteDeTravail(fabrique), horloge=lambda: MAINTENANT)
            barriere.wait()
            try:
                service.reserver(client_id, 1, datetime(2026, 10, jour, 10), datetime(2026, 10, jour, 12))
                resultats.append("succès")
            except ConflitReservation:
                resultats.append("conflit")

        fils = [threading.Thread(target=tenter, args=(client_id,)) for client_id in (1, 2)]
        for f in fils:
            f.start()
        for f in fils:
            f.join()

        assert sorted(resultats) == ["conflit", "succès"], f"jour {jour} : {resultats}"
