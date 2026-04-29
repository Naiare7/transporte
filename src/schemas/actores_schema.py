from marshmallow import Schema, fields

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    telefono = fields.Str()

class ConductorSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    licencia = fields.Str(required=True)
    telefono = fields.Str()
