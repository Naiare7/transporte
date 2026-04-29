"""
Logistics and Fleet Models - Defines vehicles, routes, and trips
"""
from src.database.db import db
from sqlalchemy import func


class Vehiculo(db.Model):
    """Transport vehicles (trucks)"""
    __tablename__ = 'vehiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    capacidad_toneladas = db.Column(db.Float, nullable=False)
    tipo_grano = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)

    def to_dict(self):
        """Convert vehicle to dictionary"""
        return {
            "id": self.id,
            "patente": self.patente,
            "capacidad": self.capacidad_toneladas,
            "tipo_grano": self.tipo_grano,
            "disponible": self.disponible
        }


class Ruta(db.Model):
    """Standard transport routes"""
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    distancia_km = db.Column(db.Float)
    tiempo_estimado_horas = db.Column(db.Float)
    
def to_dict(self):
    return {
     "id": self.id,
     "origen": self.origen,
     "destino": self.destino,
     "distancia_km": self.distancia_km,
     "tiempo_estimado": self.tiempo_estimado_horas
    }   


class Viaje(db.Model):
    """Trip operations - core of transport operations"""
    __tablename__ = 'viajes'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, default=func.now())
    se_entrego = db.Column(db.Boolean, default=False)
    fecha_salida = db.Column(db.DateTime)
    estado = db.Column(db.String(50), default='Programado')  # Programado, En Tránsito, Completado
    
    # Foreign keys
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductores.id'), nullable=False)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)
    ruta_id = db.Column(db.Integer, db.ForeignKey('rutas.id'), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relationships
    conductor = db.relationship('Conductor', backref=db.backref('viajes', lazy=True))
    vehiculo = db.relationship('Vehiculo', backref=db.backref('viajes', lazy=True))
    ruta = db.relationship('Ruta', backref=db.backref('viajes', lazy=True))
    pedido = db.relationship('Pedido', backref=db.backref('viajes', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('viajes_planificados', lazy=True))


def to_dict(self):
        return {
            "id": self.id,
            "estado": self.estado,
            "se_entrego": self.se_entrego,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "conductor_id": self.conductor_id,
            "vehiculo_id": self.vehiculo_id,
            "ruta_id": self.ruta_id
        }