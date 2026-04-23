from src.database.db import db
from src.models.operaciones import Pedido, DetallePedido
from src.models.logistica_flota import Viaje


class TransaccionService:

    @staticmethod
    def get_all_pedidos():
        return Pedido.query.all()

    @staticmethod
    def get_pedido_by_id(id):
        return Pedido.query.get(id)

    @staticmethod
    def create_pedido(data):
        pedido = Pedido(**data)
        db.session.add(pedido)
        db.session.commit()
        return pedido

    @staticmethod
    def update_pedido(pedido, data):
        for key, value in data.items():
            setattr(pedido, key, value)
        db.session.commit()
        return pedido

    @staticmethod
    def delete_pedido(pedido):
        db.session.delete(pedido)
        db.session.commit()

    @staticmethod
    def get_all_detalles():
        return DetallePedido.query.all()

    @staticmethod
    def get_detalle_by_id(id):
        return DetallePedido.query.get(id)

    @staticmethod
    def get_detalles_by_pedido(pedido_id):
        return DetallePedido.query.filter_by(pedido_id=pedido_id).all()

    @staticmethod
    def create_detalle(data):
        cantidad = data.get('cantidad', 0)
        tarifa = data.get('tarifa_flete', 0)
        data['subtotal'] = cantidad * tarifa
        detalle = DetallePedido(**data)
        db.session.add(detalle)
        db.session.commit()
        return detalle

    @staticmethod
    def update_detalle(detalle, data):
        cantidad = data.get('cantidad', detalle.cantidad)
        tarifa = data.get('tarifa_flete', detalle.tarifa_flete)
        data['subtotal'] = cantidad * tarifa
        for key, value in data.items():
            setattr(detalle, key, value)
        db.session.commit()
        return detalle

    @staticmethod
    def delete_detalle(detalle):
        db.session.delete(detalle)
        db.session.commit()

    @staticmethod
    def get_all_viajes():
        return Viaje.query.all()

    @staticmethod
    def get_viaje_by_id(id):
        return Viaje.query.get(id)

    @staticmethod
    def create_viaje(data):
        viaje = Viaje(**data)
        db.session.add(viaje)
        db.session.commit()
        return viaje

    @staticmethod
    def update_viaje(viaje, data):
        for key, value in data.items():
            setattr(viaje, key, value)
        db.session.commit()
        return viaje

    @staticmethod
    def delete_viaje(viaje):
        db.session.delete(viaje)
        db.session.commit()