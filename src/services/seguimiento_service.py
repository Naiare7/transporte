from src.database.db import db
from src.models.seguimiento import Factura, IncidenciaViaje, DetallePedido

class SeguimientoService:

    # --- MÉTODOS PARA FACTURAS ---
    @staticmethod
    def get_facturas():
        return Factura.query.all()

    @staticmethod
    def create_factura(data):
        nueva_factura = Factura(**data)
        db.session.add(nueva_factura)
        db.session.commit()
        return nueva_factura

    # --- MÉTODOS PARA INCIDENCIAS ---
    @staticmethod
    def get_all_incidencias():
        return IncidenciaViaje.query.all()

    @staticmethod
    def create_incidencia(data):
        # Asegúrate de que 'viaje_id' venga en data para evitar IntegrityError
        nueva_incidencia = IncidenciaViaje(**data)
        db.session.add(nueva_incidencia)
        db.session.commit()
        return nueva_incidencia

    # --- MÉTODOS PARA DETALLES DE PEDIDO ---
    @staticmethod
    def get_detalles_pedido():
        return DetallePedido.query.all()

    @staticmethod
    def create_detalle_pedido(data):
        # Asegúrate de que 'pedido_id' y 'descripcion_carga' vengan en data
        nuevo_detalle = DetallePedido(**data)
        db.session.add(nuevo_detalle)
        db.session.commit()
        return nuevo_detalle