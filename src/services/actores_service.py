from src.database.db import db
from src.models.actores import Cliente, Conductor


class ActoresService:

    @staticmethod
    def get_all_clientes():
        return Cliente.query.all()

    @staticmethod
    def get_cliente_by_id(id):
        return Cliente.query.get(id)

    @staticmethod
    def create_cliente(data):
        cliente = Cliente(**data)
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def update_cliente(cliente, data):
        for key, value in data.items():
            setattr(cliente, key, value)
        db.session.commit()
        return cliente

    @staticmethod
    def delete_cliente(cliente):
        db.session.delete(cliente)
        db.session.commit()

    @staticmethod
    def get_all_conductores():
        return Conductor.query.all()

    @staticmethod
    def get_conductor_by_id(id):
        return Conductor.query.get(id)

    @staticmethod
    def create_conductor(data):
        conductor = Conductor(**data)
        db.session.add(conductor)
        db.session.commit()
        return conductor

    @staticmethod
    def update_conductor(conductor, data):
        for key, value in data.items():
            setattr(conductor, key, value)
        db.session.commit()
        return conductor

    @staticmethod
    def delete_conductor(conductor):
        db.session.delete(conductor)
        db.session.commit()