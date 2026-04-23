from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from src.services.auth_service import AuthService
from src.schemas.auth_schema import UsuarioSchema, LoginSchema

bp = Blueprint('auth', __name__, url_prefix='/api')

usuario_schema = UsuarioSchema()


@bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'email': u.email, 'fecha_creacion': u.fecha_creacion} for u in usuarios]), 200


@bp.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = AuthService.get_usuario_by_id(id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email, 'fecha_creacion': usuario.fecha_creacion}), 200


@bp.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = usuario_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    if AuthService.get_usuario_by_email(data['email']):
        return jsonify({'error': 'El email ya está registrado'}), 400

    usuario = AuthService.create_usuario(data)
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email}), 201


@bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    usuario = AuthService.get_usuario_by_email(data['email'])
    if not usuario or not AuthService.verify_password(usuario, data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    token = create_access_token(identity=usuario.id)
    return jsonify({'token': token, 'usuario': {'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email}}), 200