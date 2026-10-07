import pytest
from fastapi.testclient import TestClient

from app.main import creer_app
from app.seed import peupler


@pytest.fixture
def app(tmp_path):
    application = creer_app(f"sqlite:///{tmp_path / 'test.db'}")
    peupler(application.state.fabrique_sessions)
    yield application
    application.state.engine.dispose()


@pytest.fixture
def client_http(app):
    with TestClient(app) as client:
        yield client
