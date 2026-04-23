from marshmallow import Schema, fields, validate

class VehiculoSchema(Schema):
    id = fields.Int(dump_only=True)
    patente = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    capacidad_toneladas = fields.Float(required=True)
    tipo_grano = fields.Str(validate=validate.Length(max=50), allow_none=True)
    disponible = fields.Bool()
    fecha_creacion = fields.DateTime(dump_only=True)

class RutaSchema(Schema):
    id = fields.Int(dump_only=True)
    origen = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    destino = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    distancia_km = fields.Float(allow_none=True)
    tiempo_estimado_horas = fields.Float(allow_none=True)
    fecha_creacion = fields.DateTime(dump_only=True)