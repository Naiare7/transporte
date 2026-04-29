#Gestiona la parte logística de la flota.Objetivo: Consultar vehículos, rutas y viajes del sistema.

from flask import Blueprint, request, jsonify
from src.models.logistica_flota import Vehiculo, Ruta, Viaje
from src.services.logistica_service import LogisticaService

bp = Blueprint('logistica', __name__, url_prefix='/api/logistica') #Sirve para registrar una ruta (endpoint) en la aplicación.

@bp.route('/vehiculos', methods=['GET']) #Trae todos los vehiculos de la base de datos.
def get_vehiculos(): #Recibe como parámetro los datos del vehiculo a crear.
    return jsonify(LogisticaService.get_all_vehiculos()) #Retorna los vehiculos en formato JSON.

@bp.route('/rutas', methods=['GET']) #Trae todos los vehiculos de la base de datos.
def get_rutas(): #Recibe como parámetro los datos del vehiculo a crear.
    return jsonify(LogisticaService.get_all_rutas()) #Retorna los vehiculos en formato JSON.

@bp.route('/viajes', methods=['GET']) #Trae todos los viajes de la base de datos.
def get_viajes(): #Recibe como parámetro los datos del viaje a crear.
    return jsonify(LogisticaService.get_all_viajes()) #Retorna los viajes en formato JSON.
