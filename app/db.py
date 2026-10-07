from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base


def creer_engine(url: str) -> Engine:
    """Engine SQLite dont chaque transaction démarre par BEGIN IMMEDIATE.

    BEGIN IMMEDIATE prend le verrou d'écriture dès le début : deux réservations
    concurrentes sont sérialisées, la seconde voit la première (anti-conflit).
    """
    engine = create_engine(url, connect_args={"check_same_thread": False, "timeout": 30})

    @event.listens_for(engine, "connect")
    def _desactiver_begin_implicite(connexion_dbapi, _enregistrement):
        connexion_dbapi.isolation_level = None

    @event.listens_for(engine, "begin")
    def _begin_immediate(connexion):
        connexion.exec_driver_sql("BEGIN IMMEDIATE")

    return engine


def creer_fabrique_sessions(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


def initialiser_schema(engine: Engine) -> None:
    Base.metadata.create_all(engine)
