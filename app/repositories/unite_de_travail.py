from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from app.repositories.depots import (
    SqlClientRepository,
    SqlReservationRepository,
    SqlVehiculeRepository,
)


class SqlUniteDeTravail:
    """Une transaction SQLite par bloc `with` ; annulée si `valider()` n'est pas appelé."""

    def __init__(self, fabrique_sessions: sessionmaker[Session]) -> None:
        self._fabrique = fabrique_sessions

    def __enter__(self) -> Self:
        self._session = self._fabrique()
        self.clients = SqlClientRepository(self._session)
        self.vehicules = SqlVehiculeRepository(self._session)
        self.reservations = SqlReservationRepository(self._session)
        return self

    def __exit__(self, *exc: object) -> None:
        # close() annule une transaction non validée sans expirer les objets chargés.
        self._session.close()

    def valider(self) -> None:
        self._session.commit()
