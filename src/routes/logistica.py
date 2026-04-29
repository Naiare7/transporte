from flask import Blueprint, request, jsonify
from src.services.logistica_service import LogisticaService

# Cambiamos el prefix a vacío o solo '/logistica' si app.py ya usa '/api'
bp = Blueprint('logistica', __name__)

@bp.route('/vehiculos', methods=['GET', 'POST','PUT'])
def handle_vehiculos():
    if request.method == 'POST':
        data = request.get_json()
        nuevo = LogisticaService.create_vehiculo(data)
        return jsonify(nuevo.to_dict()), 201
    
    if request.method == 'PUT':
        data = request.get_json()
        vehiculo_id = request.args.get('id')
        actualizado = LogisticaService.update_vehiculo(vehiculo_id, data)
        return jsonify(actualizado.to_dict()), 200

    # Usamos list comprehension para convertir cada objeto a diccionario
    vehiculos = LogisticaService.get_all_vehiculos()
    return jsonify([v.to_dict() for v in vehiculos]), 200

@bp.route('/rutas', methods=['GET', 'POST'])
def handle_rutas():
    if request.method == 'POST':
        data = request.get_json()
        nueva = LogisticaService.create_ruta(data)
        return jsonify(nueva.to_dict()), 201
        
    rutas = LogisticaService.get_rutas()
    return jsonify([r.to_dict() for r in rutas]), 200

@bp.route('/viajes', methods=['GET', 'POST'])
def handle_viajes():
    if request.method == 'POST':
        # Aquí podrías añadir LogisticaService.create_viaje(request.get_json())
        return jsonify({"msg": "Viaje creado"}), 201
        
    viajes = LogisticaService.get_viajes()
    return jsonify([v.to_dict() for v in viajes]), 200

@bp.route('/incidencias-viaje/<int:id>', methods=['PUT'])
def update_incidencia(id):
    # Lógica para actualizar...
    return jsonify({"msg": "Actualizado"}), 200