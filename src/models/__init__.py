from .actores import Usuario, Cliente, Conductor
from .logistica_flota import Vehiculo, Ruta, Viaje
from .seguimiento import Pedido, Factura, IncidenciaViaje, DetallePedido

# Esto facilita las importaciones masivas
__all__ = [
    "Usuario", 
    "Cliente", 
    "Conductor", 
    "Vehiculo", 
    "Ruta", 
    "Pedido", 
    "Viaje", 
    "Factura", 
    "IncidenciaViaje", 
    "DetallePedido"
]