from flask import Blueprint, request, jsonify
from src.services.actores_service import ActoresService
from src.schemas.actores_schema import UsuarioSchema, ClienteSchema, ConductorSchema    

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
conductor_schema = ConductorSchema()
conductores_schema = ConductorSchema(many=True)

bp = Blueprint('actores', __name__, url_prefix='/api')

@bp.route('/usuarios', methods=['GET', 'POST'])
def get_usuarios():
    return jsonify([usuario_schema.dump(usuario) for usuario in ActoresService.get_usuarios()])

@bp.route('/clientes', methods=['GET', 'POST'])
def get_clientes():
    return jsonify([cliente_schema.dump(cliente) for cliente in ActoresService.get_clientes()])

@bp.route('/conductores', methods=['GET', 'POST'])
def get_conductores():
    return jsonify([conductor_schema.dump(conductor) for conductor in ActoresService.get_conductores()])
