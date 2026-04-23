from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.logistica_service import LogisticaService
from src.schemas import vehiculo_schema, vehiculos_schema, ruta_schema, rutas_schema

bp = Blueprint('logistica', __name__, url_prefix='/api')


@bp.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    vehiculos = LogisticaService.get_all_vehiculos()
    return jsonify(vehiculos_schema.dump(vehiculos)), 200


@bp.route('/vehiculos/<int:id>', methods=['GET'])
def get_vehiculo(id):
    vehiculo = LogisticaService.get_vehiculo_by_id(id)
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    return jsonify(vehiculo_schema.dump(vehiculo)), 200


@bp.route('/vehiculos', methods=['POST'])
def create_vehiculo():
    try:
        data = vehiculo_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    vehiculo = LogisticaService.create_vehiculo(data)
    return jsonify(vehiculo_schema.dump(vehiculo)), 201


@bp.route('/vehiculos/<int:id>', methods=['PUT'])
def update_vehiculo(id):
    vehiculo = LogisticaService.get_vehiculo_by_id(id)
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

    try:
        data = vehiculo_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    vehiculo = LogisticaService.update_vehiculo(vehiculo, data)
    return jsonify(vehiculo_schema.dump(vehiculo)), 200


@bp.route('/vehiculos/<int:id>', methods=['DELETE'])
def delete_vehiculo(id):
    vehiculo = LogisticaService.get_vehiculo_by_id(id)
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

    LogisticaService.delete_vehiculo(vehiculo)
    return '', 204


@bp.route('/rutas', methods=['GET'])
def get_rutas():
    rutas = LogisticaService.get_all_rutas()
    return jsonify(rutas_schema.dump(rutas)), 200


@bp.route('/rutas/<int:id>', methods=['GET'])
def get_ruta(id):
    ruta = LogisticaService.get_ruta_by_id(id)
    if not ruta:
        return jsonify({'error': 'Ruta no encontrada'}), 404
    return jsonify(ruta_schema.dump(ruta)), 200


@bp.route('/rutas', methods=['POST'])
def create_ruta():
    try:
        data = ruta_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    ruta = LogisticaService.create_ruta(data)
    return jsonify(ruta_schema.dump(ruta)), 201


@bp.route('/rutas/<int:id>', methods=['PUT'])
def update_ruta(id):
    ruta = LogisticaService.get_ruta_by_id(id)
    if not ruta:
        return jsonify({'error': 'Ruta no encontrada'}), 404

    try:
        data = ruta_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    ruta = LogisticaService.update_ruta(ruta, data)
    return jsonify(ruta_schema.dump(ruta)), 200


@bp.route('/rutas/<int:id>', methods=['DELETE'])
def delete_ruta(id):
    ruta = LogisticaService.get_ruta_by_id(id)
    if not ruta:
        return jsonify({'error': 'Ruta no encontrada'}), 404

    LogisticaService.delete_ruta(ruta)
    return '', 204