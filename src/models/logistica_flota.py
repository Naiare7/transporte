from src.database.db import db
from datetime import datetime

#  ENTIDAD CAMIÓN (Tu código perfecto)
class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    capacidad_toneladas = db.Column(db.Float, nullable=False)
    tipo_grano = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "patente": self.patente,
            "capacidad": self.capacidad_toneladas,
            "tipo_grano": self.tipo_grano,
            "disponible": self.disponible
        }

#  ENTIDAD RUTA (Los trayectos estándar)
class Ruta(db.Model):
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    distancia_km = db.Column(db.Float)
    tiempo_estimado_horas = db.Column(db.Float)

#  ENTIDAD VIAJE (El centro de operaciones)
class Viaje(db.Model):
    __tablename__ = 'viajes'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_salida = db.Column(db.DateTime)
    estado = db.Column(db.String(50), default='Programado') # Programado, En Tránsito, Completado
    
    # --- CLAVES FORÁNEAS (Relacionando tablas) ---
    
    # Un viaje TIENE QUE tener un conductor asignado (Viene del archivo actores.py)
    conductor_id = db.Column(db.Integer, db.ForeignKey('conductores.id'), nullable=False)
    
    # Un viaje TIENE QUE tener un camión asignado
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)

    # Un viaje TIENE QUE tener una ruta asignada
    ruta_id = db.Column(db.Integer, db.ForeignKey('rutas.id'), nullable =False)

    # --- RELACIONES DE FLASK-SQLALCHEMY ---
    conductor = db.relationship('Conductor', backref=db.backref('viajes', lazy=True))
    vehiculo = db.relationship('Vehiculo', backref=db.backref('viajes', lazy=True))
    ruta = db.relationship('Ruta', backref=db.backref('viajes', lazy=True))