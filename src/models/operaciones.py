from src.database.db import db
from datetime import datetime

# ENTIDAD PEDIDO (La orden de transporte del cliente)
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='Pendiente')
    observaciones_entrega = db.Column(db.Text)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # OK!
    
    # RELACIONES
    cliente = db.relationship('Cliente', backref=db.backref('pedidos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('pedidos_registrados', lazy=True))

#  ENTIDAD DETALLE DE PEDIDO (Las líneas de transporte)
class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    # CAMBIO AQUÍ: En lugar de producto_id, usamos un String para describir la carga
    descripcion_carga = db.Column(db.String(150), nullable=False) # Ej: "Trigo limpio", "Pienso 20kg"
    
    cantidad = db.Column(db.Float, nullable=False) 
    unidad_medida = db.Column(db.String(20), default='Toneladas') 
    tarifa_flete = db.Column(db.Float, nullable=False) 
    subtotal = db.Column(db.Float, nullable=False) 
    requerimientos_especiales = db.Column(db.Text)
    
    # FK: Seguimos dependiendo del Pedido Padre
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    pedido = db.relationship('Pedido', backref=db.backref('detalles', lazy=True))

#  ENTIDAD INCIDENCIA DE VIAJE (Eventos inesperados en ruta)
class IncidenciaViaje(db.Model):
    __tablename__ = 'incidencias_viaje'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_incidencia = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text, nullable=False)
    gravedad = db.Column(db.String(50)) # Leve, Grave, Crítica
    
    # FK: A qué viaje pertenece la incidencia
    viaje_id = db.Column(db.Integer, db.ForeignKey('viajes.id'), nullable=False)
    
    viaje = db.relationship('Viaje', backref=db.backref('incidencias', lazy=True))

#  ENTIDAD FACTURA (Cobro final al cliente)
class Factura(db.Model):
    __tablename__ = 'facturas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    pagada = db.Column(db.Boolean, default=False)
    
    # FK: Una factura se genera a partir de un pedido completado
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False, unique=True)
    
    pedido = db.relationship('Pedido', backref=db.backref('factura', uselist=False))