from src.database.db import db
from src.models.operaciones import Producto


class ProductoService:

    @staticmethod
    def get_all():
        return Producto.query.all()

    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)

    @staticmethod
    def create(data):
        producto = Producto(**data)
        db.session.add(producto)
        db.session.commit()
        return producto

    @staticmethod
    def update(producto, data):
        for key, value in data.items():
            setattr(producto, key, value)
        db.session.commit()
        return producto

    @staticmethod
    def delete(producto):
        db.session.delete(producto)
        db.session.commit()