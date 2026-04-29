from marshmallow import Schema, fields

class ConductorSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    licencia = fields.Str(required=True)
    telefono = fields.Str()
