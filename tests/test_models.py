import pytest
from src.database.db import db
from src.models.actores import Usuario, Cliente, Conductor
from src.models.logistica_flota import Vehiculo, Viaje, Ruta
from src.models.operaciones import Pedido

# --- TESTS DE INTEGRIDAD DE USUARIOS ---
def test_crear_usuario(app):
    """Verifica que un usuario se guarde correctamente y la contraseña se cifre"""
    with app.app_context():
        user = Usuario(nombre="test_user", email="test@grano.com", password="123")
        db.session.add(user)
        db.session.commit()

        usuario_db = Usuario.query.filter_by(email="test@grano.com").first()
        assert usuario_db is not None
        assert usuario_db.email == "test@grano.com"
        assert usuario_db.check_password("123")

# --- TESTS DE ACTORES (Clientes y Conductores) ---
def test_relacion_cliente_pedido(app):
    """Verifica que un pedido esté correctamente asociado a un cliente"""
    with app.app_context():
        usuario = Usuario(nombre="ClienteTest", email="cliente@test.com", password="123")
        db.session.add(usuario)
        db.session.commit()

        cliente = Cliente(razon_social="Agro S.A.", cif_nif="20-12345-9")
        db.session.add(cliente)
        db.session.commit()

        pedido = Pedido(cliente_id=cliente.id, usuario_id=usuario.id, estado="Pendiente")
        db.session.add(pedido)
        db.session.commit()

        assert pedido.cliente.razon_social == "Agro S.A."
        assert len(cliente.pedidos) == 1

# --- TESTS DE LOGÍSTICA (Vehículos y Viajes) ---
def test_validar_capacidad_vehiculo(app):
    """Prueba que los campos numéricos de los vehículos funcionen"""
    with app.app_context():
        camion = Vehiculo(patente="AF123JK", capacidad_toneladas=32000, tipo_grano="Maíz")
        db.session.add(camion)
        db.session.commit()

        assert camion.capacidad_toneladas >= 0
        assert "AF123JK" in camion.patente

# --- TESTS DE TRANSACCIONES (El flujo del Viaje) ---
def test_flujo_viaje_completo(app):
    """Verifica la unión de Conductor, Vehículo y Pedido en un Viaje"""
    with app.app_context():
        usuario = Usuario(nombre="user_viaje", email="user_viaje@test.com", password="123")
        chofer = Conductor(nombre_completo="Carlos Perez", dni="12345678", carnet_conducir="L123")
        camion = Vehiculo(patente="TRUCK1", capacidad_toneladas=30000, tipo_grano="Volvo")
        ruta = Ruta(origen="Origen", destino="Destino", distancia_km=250)
        cliente = Cliente(razon_social="Transportes SRL", cif_nif="20-12345678-1")

        db.session.add_all([usuario, chofer, camion, ruta, cliente])
        db.session.commit()

        pedido = Pedido(cliente_id=cliente.id, usuario_id=usuario.id, estado="Programado")
        db.session.add(pedido)
        db.session.commit()

        viaje = Viaje(
            conductor_id=chofer.id,
            vehiculo_id=camion.id,
            ruta_id=ruta.id,
            pedido_id=pedido.id,
            usuario_id=usuario.id,
            estado="Programado"
        )
        db.session.add(viaje)
        db.session.commit()

        assert viaje.conductor.nombre_completo == "Carlos Perez"
        assert viaje.vehiculo.patente == "TRUCK1"
        assert viaje.pedido.id == pedido.id
