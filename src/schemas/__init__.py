from .actores_schema import ClienteSchema
from .conductor_schema import ConductorSchema
from .logistica_schema import VehiculoSchema, RutaSchema, ViajeSchema
from .seguimiento_schema import IncidenciaViajeSchema, FacturaSchema
from .transacciones_schema import PedidoSchema
from .auth_schema import UsuarioSchema, LoginSchema

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

conductor_schema = ConductorSchema()
conductores_schema = ConductorSchema(many=True)

vehiculo_schema = VehiculoSchema()
vehiculos_schema = VehiculoSchema(many=True)

ruta_schema = RutaSchema()
rutas_schema = RutaSchema(many=True)

viaje_schema = ViajeSchema()
viajes_schema = ViajeSchema(many=True)

incidencia_schema = IncidenciaViajeSchema()
incidencias_schema = IncidenciaViajeSchema(many=True)

factura_schema = FacturaSchema()
facturas_schema = FacturaSchema(many=True)

pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

login_schema = LoginSchema()
