"""
Actors Models - Defines database models for users, clients, and drivers
"""
from src.database.db import db
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash


class Usuario(db.Model):
    """System users (administrators)"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=func.now())

    @property
    def password(self):
        """Password is write-only"""
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, password):
        """Hash password on set"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)


class Cliente(db.Model):
    """Clients who request transport services"""
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(150), nullable=False)
    cif_nif = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(250))
    
    # Relationship: A client has many orders
    # pedidos = db.relationship('Pedido', backref='cliente', lazy=True)


class Conductor(db.Model):
    """Drivers who operate the vehicles"""
    __tablename__ = 'conductores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    carnet_conducir = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    disponible = db.Column(db.Boolean, default=True)  # Available or on route
