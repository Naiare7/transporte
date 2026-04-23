from werkzeug.security import generate_password_hash, check_password_hash
from src.database.db import db
from src.models.actores import Usuario


class AuthService:

    @staticmethod
    def create_usuario(data):
        data['password_hash'] = generate_password_hash(data.pop('password'))
        usuario = Usuario(**data)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def get_usuario_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def get_usuario_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def verify_password(usuario, password):
        return check_password_hash(usuario.password_hash, password)