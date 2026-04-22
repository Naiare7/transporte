from flask import Blueprint, jsonify
from ..database.db import db
from ..models import actores, logistica_flota, operaciones

main = Blueprint('routes_main', __name__)

