from src.database.db import db
from src.models.logistica_flota import Vehiculo, Ruta


class LogisticaService:

    @staticmethod
    def get_all_vehiculos():
        return Vehiculo.query.all()

    @staticmethod
    def get_vehiculo_by_id(id):
        return Vehiculo.query.get(id)

    @staticmethod
    def create_vehiculo(data):
        vehiculo = Vehiculo(**data)
        db.session.add(vehiculo)
        db.session.commit()
        return vehiculo

    @staticmethod
    def update_vehiculo(vehiculo, data):
        for key, value in data.items():
            setattr(vehiculo, key, value)
        db.session.commit()
        return vehiculo

    @staticmethod
    def delete_vehiculo(vehiculo):
        db.session.delete(vehiculo)
        db.session.commit()

    @staticmethod
    def get_all_rutas():
        return Ruta.query.all()

    @staticmethod
    def get_ruta_by_id(id):
        return Ruta.query.get(id)

    @staticmethod
    def create_ruta(data):
        ruta = Ruta(**data)
        db.session.add(ruta)
        db.session.commit()
        return ruta

    @staticmethod
    def update_ruta(ruta, data):
        for key, value in data.items():
            setattr(ruta, key, value)
        db.session.commit()
        return ruta

    @staticmethod
    def delete_ruta(ruta):
        db.session.delete(ruta)
        db.session.commit()