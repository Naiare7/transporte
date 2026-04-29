from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.actores_service import ActoresService
from src.schemas import (
    cliente_schema, clientes_schema,
    conductor_schema, conductores_schema
)

bp = Blueprint('actores', __name__, url_prefix='/api')


@bp.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = ActoresService.get_all_clientes()
    return jsonify(clientes_schema.dump(clientes)), 200


@bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = ActoresService.get_cliente_by_id(id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    return jsonify(cliente_schema.dump(cliente)), 200


@bp.route('/clientes', methods=['POST'])
def create_cliente():
    try:
        data = cliente_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    cliente = ActoresService.create_cliente(data)
    return jsonify(cliente_schema.dump(cliente)), 201


@bp.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    cliente = ActoresService.get_cliente_by_id(id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        data = cliente_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    cliente = ActoresService.update_cliente(cliente, data)
    return jsonify(cliente_schema.dump(cliente)), 200


@bp.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = ActoresService.get_cliente_by_id(id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    ActoresService.delete_cliente(cliente)
    return '', 204


@bp.route('/conductores', methods=['GET'])
def get_conductores():
    conductores = ActoresService.get_all_conductores()
    return jsonify(conductores_schema.dump(conductores)), 200


@bp.route('/conductores/<int:id>', methods=['GET'])
def get_conductor(id):
    conductor = ActoresService.get_conductor_by_id(id)
    if not conductor:
        return jsonify({'error': 'Conductor no encontrado'}), 404
    return jsonify(conductor_schema.dump(conductor)), 200


@bp.route('/conductores', methods=['POST'])
def create_conductor():
    try:
        data = conductor_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    conductor = ActoresService.create_conductor(data)
    return jsonify(conductor_schema.dump(conductor)), 201


@bp.route('/conductores/<int:id>', methods=['PUT'])
def update_conductor(id):
    conductor = ActoresService.get_conductor_by_id(id)
    if not conductor:
        return jsonify({'error': 'Conductor no encontrado'}), 404

    try:
        data = conductor_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    conductor = ActoresService.update_conductor(conductor, data)
    return jsonify(conductor_schema.dump(conductor)), 200


@bp.route('/conductores/<int:id>', methods=['DELETE'])
def delete_conductor(id):
    conductor = ActoresService.get_conductor_by_id(id)
    if not conductor:
        return jsonify({'error': 'Conductor no encontrado'}), 404

    ActoresService.delete_conductor(conductor)
    return '', 204