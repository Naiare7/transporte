from src.database.db import db
from src.models.operaciones import IncidenciaViaje, DetallePedido


class SeguimientoService:

    @staticmethod
    def get_all_incidencias():
        return IncidenciaViaje.query.all()

    @staticmethod
    def get_incidencia_by_id(id):
        return IncidenciaViaje.query.get(id)

    @staticmethod
    def get_incidencias_by_viaje(viaje_id):
        return IncidenciaViaje.query.filter_by(viaje_id=viaje_id).all()

    @staticmethod
    def create_incidencia(data):
        incidencia = IncidenciaViaje(**data)
        db.session.add(incidencia)
        db.session.commit()
        return incidencia

    @staticmethod
    def delete_incidencia(incidencia):
        db.session.delete(incidencia)
        db.session.commit()

    @staticmethod
    def get_informe_by_viaje(viaje_id):
        return InformeDescarga.query.filter_by(viaje_id=viaje_id).first()

    @staticmethod
    def create_informe(data):
        informe = InformeDescarga(**data)
        db.session.add(informe)
        db.session.commit()
        return informe

    @staticmethod
    def update_informe(informe, data):
        for key, value in data.items():
            setattr(informe, key, value)
        db.session.commit()
        return informe

    @staticmethod
    def get_all_facturas():
        return Factura.query.all()

    @staticmethod
    def get_factura_by_id(id):
        return Factura.query.get(id)

    @staticmethod
    def get_factura_by_pedido(pedido_id):
        return Factura.query.filter_by(pedido_id=pedido_id).first()

    @staticmethod
    def create_factura(data):
        total = 0
        detalles = DetallePedido.query.filter_by(pedido_id=data['pedido_id']).all()
        for d in detalles:
            total += d.subtotal
        data['total'] = total
        factura = Factura(**data)
        db.session.add(factura)
        db.session.commit()
        return factura

    @staticmethod
    def update_factura(factura, data):
        for key, value in data.items():
            setattr(factura, key, value)
        db.session.commit()
        return factura