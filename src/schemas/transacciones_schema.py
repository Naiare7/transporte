from marshmallow import Schema, fields, validate

class PedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    cliente_id = fields.Int(required=True)
    estado = fields.Str(validate=validate.Length(max=50))
    observaciones_entrega = fields.Str(allow_none=True)
    fecha_pedido = fields.DateTime(dump_only=True)

class DetallePedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    pedido_id = fields.Int(required=True)
    descripcion_carga = fields.Str(required=True, validate=validate.Length(min=1, max=150)) 
    cantidad = fields.Float(required=True)
    unidad_medida = fields.Str(validate=validate.Length(max=20))
    tarifa_flete = fields.Float(required=True)
    subtotal = fields.Float(dump_only=True)
    requerimientos_especiales = fields.Str(allow_none=True)

class ViajeSchema(Schema):
    id = fields.Int(dump_only=True)
    conductor_id = fields.Int(required=True)
    vehiculo_id = fields.Int(required=True)
    ruta_id = fields.Int(required=True)
    estado = fields.Str(validate=validate.Length(max=50))
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_salida = fields.DateTime(allow_none=True)