from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    password_hash = fields.Str(dump_only=True)
    fecha_creacion = fields.DateTime(dump_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)