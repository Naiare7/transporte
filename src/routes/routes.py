from flask import Blueprint, request, jsonify
from src.database.db import db
from src.models.actores import Cliente
from src.models.logistica_flota import Vehiculo # Importamos tu Vehículo desde su archivo correcto

# Creamos el "Plano" (Blueprint) de nuestras rutas
api_bp = Blueprint('api', __name__)
