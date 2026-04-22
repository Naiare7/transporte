from flask import Blueprint, jsonify
from ..database.db import db
from ..models import actores, vehiculos, operaciones

main = Blueprint('routes_main', __name__)

@main.route('/camiones', methods=['GET'])
def get_camiones():
    lista_camiones = Camion.query.all()
    return jsonify([c.to_dict() for c in lista_camiones]), 200
