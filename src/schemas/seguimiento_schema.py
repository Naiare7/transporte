from marshmallow import Schema, fields, validate

class IncidenciaViajeSchema(Schema):
    id = fields.Int(dump_only=True)
    viaje_id = fields.Int(required=True)
    descripcion = fields.Str(required=True)
    gravedad = fields.Str(validate=validate.Length(max=50))
    fecha_incidencia = fields.DateTime(dump_only=True)

class FacturaSchema(Schema):
    id = fields.Int(dump_only=True)
    pedido_id = fields.Int(required=True)
    total = fields.Float(dump_only=True)
    pagada = fields.Bool()
    fecha_emision = fields.DateTime(dump_only=True)