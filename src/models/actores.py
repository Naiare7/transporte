from src.database.db import db
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

#  ENTIDAD USUARIO (Administradores)
class Usuario(db.Model):
    __tablename__ = 'usuarios' # Nombre de la tabla en PostgreSQL
    
    # Definición de Atributos (Columnas)
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=func.now())

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#  ENTIDAD CLIENTE (Los que piden el transporte)
class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(150), nullable=False)
    cif_nif = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(250))
    
    # RELACIÓN: Un cliente tendrá muchos pedidos (Lo conectaremos más adelante)
    # pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

#  ENTIDAD CONDUCTOR (Los que manejan los camiones)
class Conductor(db.Model):
    __tablename__ = 'conductores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    carnet_conducir = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    disponible = db.Column(db.Boolean, default=True) # Para saber si está en ruta o libre


    