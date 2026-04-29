from flask import Blueprint, request, jsonify
from src.models.operaciones import Pedido, DetallePedido, Factura
from src.services.transaccion_service import TransaccionService

bp = Blueprint('transacciones', __name__, url_prefix='/api/transacciones')

@bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    return jsonify(TransaccionService.get_all_pedidos())

@bp.route('/facturas', methods=['GET'])
def get_facturas():
    return jsonify(TransaccionService.get_all_facturas())
