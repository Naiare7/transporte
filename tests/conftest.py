import pytest
from src.app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:" # Base de datos rápida en memoria para tests
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()