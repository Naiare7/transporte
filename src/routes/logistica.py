from flask import Blueprint, request, jsonify
from src.models.logistica_flota import Vehiculo, Ruta, Viaje
from src.services.logistica_service import LogisticaService

bp = Blueprint('logistica', __name__, url_prefix='/api/logistica')

@bp.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    return jsonify(LogisticaService.get_all_vehiculos())

@bp.route('/rutas', methods=['GET'])
def get_rutas():
    return jsonify(LogisticaService.get_all_rutas())

@bp.route('/viajes', methods=['GET'])
def get_viajes():
    return jsonify(LogisticaService.get_all_viajes())
