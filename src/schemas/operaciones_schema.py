from marshmallow import Schema, fields, validate

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    categoria = fields.Str(validate=validate.Length(max=50), allow_none=True)
    requiere_limpieza_especial = fields.Bool()
    fecha_creacion = fields.DateTime(dump_only=True)