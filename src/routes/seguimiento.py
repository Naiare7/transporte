from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.seguimiento_service import SeguimientoService
from src.schemas.seguimiento_schema import IncidenciaViajeSchema, FacturaSchema

bp = Blueprint('seguimiento', __name__, url_prefix='/api')

incidencia_schema = IncidenciaViajeSchema()
incidencias_schema = IncidenciaViajeSchema(many=True)
factura_schema = FacturaSchema()
facturas_schema = FacturaSchema(many=True)


@bp.route('/incidencias-viaje', methods=['GET'])
def get_incidencias():
    incidencias = SeguimientoService.get_all_incidencias()
    return jsonify(incidencias_schema.dump(incidencias)), 200


@bp.route('/incidencias-viaje/<int:id>', methods=['GET'])
def get_incidencia(id):
    incidencia = SeguimientoService.get_incidencia_by_id(id)
    if not incidencia:
        return jsonify({'error': 'Incidencia no encontrada'}), 404
    return jsonify(incidencia_schema.dump(incidencia)), 200


@bp.route('/viajes/<int:viaje_id>/incidencias', methods=['GET'])
def get_viaje_incidencias(viaje_id):
    incidencias = SeguimientoService.get_incidencias_by_viaje(viaje_id)
    return jsonify(incidencias_schema.dump(incidencias)), 200


@bp.route('/incidencias-viaje', methods=['POST'])
def create_incidencia():
    try:
        data = incidencia_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    incidencia = SeguimientoService.create_incidencia(data)
    return jsonify(incidencia_schema.dump(incidencia)), 201


@bp.route('/incidencias-viaje/<int:id>', methods=['DELETE'])
def delete_incidencia(id):
    incidencia = SeguimientoService.get_incidencia_by_id(id)
    if not incidencia:
        return jsonify({'error': 'Incidencia no encontrada'}), 404

    SeguimientoService.delete_incidencia(incidencia)
    return '', 204


@bp.route('/facturas', methods=['GET'])
def get_facturas():
    facturas = SeguimientoService.get_all_facturas()
    return jsonify(facturas_schema.dump(facturas)), 200


@bp.route('/facturas/<int:id>', methods=['GET'])
def get_factura(id):
    factura = SeguimientoService.get_factura_by_id(id)
    if not factura:
        return jsonify({'error': 'Factura no encontrada'}), 404
    return jsonify(factura_schema.dump(factura)), 200


@bp.route('/pedidos/<int:pedido_id>/factura', methods=['GET'])
def get_pedido_factura(pedido_id):
    factura = SeguimientoService.get_factura_by_pedido(pedido_id)
    if not factura:
        return jsonify({'error': 'Factura no encontrada para este pedido'}), 404
    return jsonify(factura_schema.dump(factura)), 200


@bp.route('/facturas', methods=['POST'])
def create_factura():
    try:
        data = factura_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    if SeguimientoService.get_factura_by_pedido(data['pedido_id']):
        return jsonify({'error': 'Este pedido ya tiene una factura'}), 400

    factura = SeguimientoService.create_factura(data)
    return jsonify(factura_schema.dump(factura)), 201


@bp.route('/facturas/<int:id>', methods=['PUT'])
def update_factura(id):
    factura = SeguimientoService.get_factura_by_id(id)
    if not factura:
        return jsonify({'error': 'Factura no encontrada'}), 404

    try:
        data = factura_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    factura = SeguimientoService.update_factura(factura, data)
    return jsonify(factura_schema.dump(factura)), 200