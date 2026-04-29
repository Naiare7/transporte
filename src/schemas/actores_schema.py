from marshmallow import Schema, fields, validate

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    razon_social = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    cif_nif = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    telefono = fields.Str(validate=validate.Length(max=20), allow_none=True)
    direccion = fields.Str(validate=validate.Length(max=250), allow_none=True)
    fecha_creacion = fields.DateTime(dump_only=True)