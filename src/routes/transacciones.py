from flask import Blueprint, request, jsonify
from src.services.transaccion_service import TransaccionService

bp = Blueprint('transacciones', __name__)

@bp.route('/pedidos', methods=['GET', 'POST'])
def handle_pedidos():
    if request.method == 'POST':
        data = request.get_json()
        nuevo = TransaccionService.create_pedido(data)
        return jsonify(nuevo.to_dict()), 201
    return jsonify([p.to_dict() for p in TransaccionService.get_all_pedidos()]), 200

@bp.route('/detalles-pedido', methods=['GET', 'POST'])
def handle_detalles_pedido():
    if request.method == 'POST':
        data = request.get_json()
        nuevo = TransaccionService.create_detalle(data)
        return jsonify(nuevo.to_dict()), 201
    return jsonify([d.to_dict() for d in TransaccionService.get_all_detalles()]), 200

@bp.route('/pedidos/<int:pedido_id>/detalles', methods=['GET'])
def get_pedido_detalles(pedido_id):
    detalles = TransaccionService.get_detalles_by_pedido(pedido_id)
    return jsonify([d.to_dict() for d in detalles]), 200