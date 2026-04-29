from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.transaccion_service import TransaccionService
from src.models.operaciones import Pedido, DetallePedido
from src.models.logistica_flota import Viaje
from src.schemas.transacciones_schema import PedidoSchema, DetallePedidoSchema, ViajeSchema

bp = Blueprint('transacciones', __name__, url_prefix='/api')

pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)
detalle_schema = DetallePedidoSchema()
detalles_schema = DetallePedidoSchema(many=True)
viaje_schema = ViajeSchema()
viajes_schema = ViajeSchema(many=True)


@bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = TransaccionService.get_all_pedidos()
    return jsonify(pedidos_schema.dump(pedidos)), 200


@bp.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    pedido = TransaccionService.get_pedido_by_id(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    return jsonify(pedido_schema.dump(pedido)), 200


@bp.route('/pedidos', methods=['POST'])
def create_pedido():
    try:
        data = pedido_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    pedido = TransaccionService.create_pedido(data)
    return jsonify(pedido_schema.dump(pedido)), 201


@bp.route('/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    pedido = TransaccionService.get_pedido_by_id(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404

    try:
        data = pedido_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    pedido = TransaccionService.update_pedido(pedido, data)
    return jsonify(pedido_schema.dump(pedido)), 200


@bp.route('/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    pedido = TransaccionService.get_pedido_by_id(id)
    if not pedido:
        return jsonify({'error': 'Pedido no encontrado'}), 404

    TransaccionService.delete_pedido(pedido)
    return '', 204


@bp.route('/pedidos/<int:id>/detalles', methods=['GET'])
def get_pedido_detalles(id):
    detalles = TransaccionService.get_detalles_by_pedido(id)
    return jsonify(detalles_schema.dump(detalles)), 200


@bp.route('/detalles-pedido', methods=['GET'])
def get_detalles():
    detalles = TransaccionService.get_all_detalles()
    return jsonify(detalles_schema.dump(detalles)), 200


@bp.route('/detalles-pedido', methods=['POST'])
def create_detalle():
    try:
        data = detalle_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    detalle = TransaccionService.create_detalle(data)
    return jsonify(detalle_schema.dump(detalle)), 201


@bp.route('/detalles-pedido/<int:id>', methods=['PUT'])
def update_detalle(id):
    detalle = TransaccionService.get_detalle_by_id(id)
    if not detalle:
        return jsonify({'error': 'Detalle no encontrado'}), 404

    try:
        data = detalle_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    detalle = TransaccionService.update_detalle(detalle, data)
    return jsonify(detalle_schema.dump(detalle)), 200


@bp.route('/detalles-pedido/<int:id>', methods=['DELETE'])
def delete_detalle(id):
    detalle = TransaccionService.get_detalle_by_id(id)
    if not detalle:
        return jsonify({'error': 'Detalle no encontrado'}), 404

    TransaccionService.delete_detalle(detalle)
    return '', 204


@bp.route('/viajes', methods=['GET'])
def get_viajes():
    viajes = TransaccionService.get_all_viajes()
    return jsonify(viajes_schema.dump(viajes)), 200


@bp.route('/viajes/<int:id>', methods=['GET'])
def get_viaje(id):
    viaje = TransaccionService.get_viaje_by_id(id)
    if not viaje:
        return jsonify({'error': 'Viaje no encontrado'}), 404
    return jsonify(viaje_schema.dump(viaje)), 200


@bp.route('/viajes', methods=['POST'])
def create_viaje():
    try:
        data = viaje_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    viaje = TransaccionService.create_viaje(data)
    return jsonify(viaje_schema.dump(viaje)), 201


@bp.route('/viajes/<int:id>', methods=['PUT'])
def update_viaje(id):
    viaje = TransaccionService.get_viaje_by_id(id)
    if not viaje:
        return jsonify({'error': 'Viaje no encontrado'}), 404

    try:
        data = viaje_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    viaje = TransaccionService.update_viaje(viaje, data)
    return jsonify(viaje_schema.dump(viaje)), 200


@bp.route('/viajes/<int:id>', methods=['DELETE'])
def delete_viaje(id):
    viaje = TransaccionService.get_viaje_by_id(id)
    if not viaje:
        return jsonify({'error': 'Viaje no encontrado'}), 404

    TransaccionService.delete_viaje(viaje)
    return '', 204


@bp.route('/viajes/<int:id>/estado', methods=['PATCH'])
def update_viaje_estado(id):
    viaje = TransaccionService.get_viaje_by_id(id)
    if not viaje:
        return jsonify({'error': 'Viaje no encontrado'}), 404

    data = request.json
    if 'estado' not in data:
        return jsonify({'error': 'Campo estado requerido'}), 400

    viaje = TransaccionService.update_viaje(viaje, {'estado': data['estado']})
    return jsonify(viaje_schema.dump(viaje)), 200