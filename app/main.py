import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import reservations
from app.db import creer_engine, creer_fabrique_sessions, initialiser_schema
from app.domain.erreurs import ErreurMetier

URL_PAR_DEFAUT = "sqlite:///./location.db"


def creer_app(url_base: str | None = None) -> FastAPI:
    engine = creer_engine(url_base or os.environ.get("DATABASE_URL", URL_PAR_DEFAUT))
    initialiser_schema(engine)

    app = FastAPI(title="Location de vélos et trottinettes")
    app.state.engine = engine
    app.state.fabrique_sessions = creer_fabrique_sessions(engine)
    app.include_router(reservations.router)

    @app.exception_handler(ErreurMetier)
    async def gerer_erreur_metier(_request: Request, exc: ErreurMetier) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status, content={"erreur": exc.code, "message": exc.message}
        )

    return app
