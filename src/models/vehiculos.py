from src.database.db import db

class Camion(db.Model):
    __tablename__ = 'camiones'
    
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