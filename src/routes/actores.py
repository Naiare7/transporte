from flask import Blueprint, request, jsonify
from src.models.actores import Usuario, Cliente, Conductor
from src.services.actores_service import ActoresService

bp = Blueprint('actores', __name__, url_prefix='/api/actores')

@bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    return jsonify(ActoresService.get_all_usuarios())

@bp.route('/clientes', methods=['GET'])
def get_clientes():
    return jsonify(ActoresService.get_all_clientes())

@bp.route('/conductores', methods=['GET'])
def get_conductores():
    return jsonify(ActoresService.get_all_conductores())
