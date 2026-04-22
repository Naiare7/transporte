from flask import jsonify
from src.app import app
from src.models.vehiculos import Camion
from src.database.db import db

@app.route('/camiones', methods=['GET'])
def get_camiones():
    lista_camiones = Camion.query.all()
    return jsonify([c.to_dict() for c in lista_camiones]), 200