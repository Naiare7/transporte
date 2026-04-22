from src.database.db import db
from datetime import datetime

#  ENTIDAD PRODUCTO (Catálogo de lo que transportamos, NO lo que vendemos)
class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False) # Ej: Trigo, Maíz, Pienso cerdos
    categoria = db.Column(db.String(50)) # Ej: Grano agrícola, Pienso animal
    requiere_limpieza_especial = db.Column(db.Boolean, default=False) # Clave para la logística

# ENTIDAD PEDIDO (La orden de transporte del cliente)
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='Pendiente')
    observaciones_entrega = db.Column(db.Text)

    # FK: El pedido pertenece a un cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    cliente = db.relationship('Cliente', backref=db.backref('pedidos', lazy=True))

#  ENTIDAD DETALLE DE PEDIDO (Las líneas de transporte)
class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=False) # Cantidad a mover
    unidad_medida = db.Column(db.String(20), default='Toneladas') # Ej: Toneladas, Viajes, Metros Cúbicos
    tarifa_flete = db.Column(db.Float, nullable=False) # Precio por la unidad elegida
    subtotal = db.Column(db.Float, nullable=False) # cantidad * tarifa_flete
    requerimientos_especiales = db.Column(db.Text)
    
 # FKs: Qué llevamos y en qué pedido
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    
    pedido = db.relationship('Pedido', backref=db.backref('detalles', lazy=True))
    producto = db.relationship('Producto', backref=db.backref('detalles_pedido', lazy=True))

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

#  ENTIDAD INFORME DE DESCARGA (Albarán de llegada y peso real)
class InformeDescarga(db.Model):
    __tablename__ = 'informes_descarga'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_descarga = db.Column(db.DateTime, default=datetime.utcnow)
    toneladas_entregadas_reales = db.Column(db.Float, nullable=False) # A veces se pierde grano por el camino (mermas)
    porcentaje_humedad = db.Column(db.Float) # Muy importante en el grano
    
    # FK: De qué viaje es este informe
    viaje_id = db.Column(db.Integer, db.ForeignKey('viajes.id'), nullable=False, unique=True)
    
    viaje = db.relationship('Viaje', backref=db.backref('informe_descarga', uselist=False))

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