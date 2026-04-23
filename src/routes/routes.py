from flask import Blueprint, request, jsonify
from src.database.db import db
from src.models.actores import Cliente
from src.models.logistica_flota import Vehiculo # Importamos tu Vehículo desde su archivo correcto

# Creamos el "Plano" (Blueprint) de nuestras rutas
api_bp = Blueprint('api', __name__)
from flask import Blueprint, jsonify
from ..database.db import db
from ..models import actores, logistica_flota, operaciones

main = Blueprint('routes_main', __name__)

