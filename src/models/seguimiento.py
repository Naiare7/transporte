"""
Operations Models - Defines orders, order details, invoices, and incidents
"""
from src.database.db import db
from sqlalchemy import func


class Pedido(db.Model):
    """Transport orders requested by clients"""
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, default=func.now())
    estado = db.Column(db.String(50), default='Pendiente')
    observaciones_entrega = db.Column(db.Text)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relationships
    cliente = db.relationship('Cliente', backref=db.backref('pedidos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('pedidos_registrados', lazy=True))

def to_dict(self):
    return {
        "id": self.id,
        "fecha_pedido": self.fecha_pedido.isoformat() if self.fecha_pedido else None,
        "estado": self.estado,
        "observaciones_entrega": self.observaciones_entrega
    }

class DetallePedido(db.Model):
    """Order line items - specific cargo details"""
    __tablename__ = 'detalles_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion_carga = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad_medida = db.Column(db.String(20), default='Toneladas')
    tarifa_flete = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    requerimientos_especiales = db.Column(db.Text)
    
    # Foreign key to parent order
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    pedido = db.relationship('Pedido', backref=db.backref('detalles', lazy=True))

def to_dict(self):
    return {
        "id": self.id,
        "descripcion_carga": self.descripcion_carga,
        "cantidad": self.cantidad,
        "unidad_medida": self.unidad_medida,
        "tarifa_flete": self.tarifa_flete,
        "subtotal": self.subtotal,
        "requerimientos_especiales": self.requerimientos_especiales
    }

class IncidenciaViaje(db.Model):
    """Unexpected events during trips"""
    __tablename__ = 'incidencias_viaje'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_incidencia = db.Column(db.DateTime, default=func.now())
    descripcion = db.Column(db.Text, nullable=False)
    gravedad = db.Column(db.String(50))  # Leve, Grave, Crítica
    
    # Foreign key to trip
    viaje_id = db.Column(db.Integer, db.ForeignKey('viajes.id'), nullable=False)
    viaje = db.relationship('Viaje', backref=db.backref('incidencias', lazy=True))

def to_dict(self):
    return {
        "id": self.id,
        "fecha_incidencia": self.fecha_incidencia.isoformat() if self.fecha_incidencia else None,
        "descripcion": self.descripcion,
        "gravedad": self.gravedad,
        "viaje_id": self.viaje_id
    }

class Factura(db.Model):
    """Billing - final charges to clients"""
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_emision = db.Column(db.DateTime, default=func.now())
    total = db.Column(db.Float, nullable=False)
    pagada = db.Column(db.Boolean, default=False)
    
    # Foreign key to completed order
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False, unique=True)
    pedido = db.relationship('Pedido', backref=db.backref('factura', uselist=False))

def to_dict(self):
    return {
        "id": self.id,
        "fecha_emision": self.fecha_emision.isoformat() if self.fecha_emision else None,
        "total": self.total,
        "pagada": self.pagada
    }