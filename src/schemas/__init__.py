from .actores_schema import ClienteSchema
from .conductor_schema import ConductorSchema
from .logistica_schema import VehiculoSchema, RutaSchema

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

conductor_schema = ConductorSchema()
conductores_schema = ConductorSchema(many=True)

vehiculo_schema = VehiculoSchema()
vehiculos_schema = VehiculoSchema(many=True)

ruta_schema = RutaSchema()
rutas_schema = RutaSchema(many=True)