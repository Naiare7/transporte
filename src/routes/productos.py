from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.producto_service import ProductoService
from src.schemas import producto_schema, productos_schema

bp = Blueprint('operaciones', __name__, url_prefix='/api')


@bp.route('/productos', methods=['GET'])
def get_productos():
    productos = ProductoService.get_all()
    return jsonify(productos_schema.dump(productos)), 200


@bp.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = ProductoService.get_by_id(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify(producto_schema.dump(producto)), 200


@bp.route('/productos', methods=['POST'])
def create_producto():
    try:
        data = producto_schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    producto = ProductoService.create(data)
    return jsonify(producto_schema.dump(producto)), 201


@bp.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = ProductoService.get_by_id(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    try:
        data = producto_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    producto = ProductoService.update(producto, data)
    return jsonify(producto_schema.dump(producto)), 200


@bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = ProductoService.get_by_id(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    ProductoService.delete(producto)
    return '', 204