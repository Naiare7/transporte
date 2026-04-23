from marshmallow import Schema, fields, validate

class ConductorSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_completo = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    dni = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    carnet_conducir = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    telefono = fields.Str(validate=validate.Length(max=20), allow_none=True)
    disponible = fields.Bool()
    fecha_creacion = fields.DateTime(dump_only=True)