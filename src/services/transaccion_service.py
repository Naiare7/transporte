from src.database.db import db
from src.models.seguimiento import Pedido, DetallePedido
from src.models.logistica_flota import Viaje

class TransaccionService:
    @staticmethod
    def get_all_pedidos():
        return Pedido.query.all()

    @staticmethod
    def get_pedido_by_id(id):
        return db.session.get(Pedido, id)

    @staticmethod
    def create_pedido(data):
        pedido = Pedido(**data)
        db.session.add(pedido)
        db.session.commit()
        return pedido

    @staticmethod
    def get_all_detalles():
        return DetallePedido.query.all()

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