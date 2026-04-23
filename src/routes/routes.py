from flask import Blueprint, jsonify
from ..models.logistica_flota import Vehiculo

main = Blueprint('routes_main', __name__)

@main.route('/camiones', methods=['GET'])
def get_camiones():
    lista_camiones = Vehiculo.query.all()
    return jsonify([c.to_dict() for c in lista_camiones]), 200