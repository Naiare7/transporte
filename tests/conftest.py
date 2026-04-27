import pytest
from src.app import create_app
from src.database.db import db

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        # CREAR USUARIO DE PRUEBA AQUÍ
        from src.models import Usuario
        if not Usuario.query.filter_by(email="admin@test.com").first():
            user = Usuario(nombre="Admin", email="admin@test.com", password="123")
            db.session.add(user)
            db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()