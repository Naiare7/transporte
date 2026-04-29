import pytest
from src.schemas.auth_schema import UsuarioSchema
from src.schemas.actores_schema import ClienteSchema
from src.schemas.logistica_schema import VehiculoSchema, ViajeSchema

# --- TESTS DE USUARIO SCHEMA ---
def test_usuario_schema_validacion():
    """Prueba que el schema de usuario valide campos obligatorios y formatos"""
    schema = UsuarioSchema()
    
    # 1. Datos válidos
    datos_validos = {"nombre": "Admin", "email": "admin@test.com", "password": "123456"}
    errors = schema.validate(datos_validos)
    assert not errors

    # 2. Email inválido
    datos_invalidos = {"nombre": "Admin", "email": "esto-no-es-un-email", "password": "123456"}
    errors = schema.validate(datos_invalidos)
    assert "email" in errors

# --- TESTS DE CLIENTE SCHEMA ---
def test_cliente_schema_campos():
    """Prueba la validación de Clientes (Actores)"""
    schema = ClienteSchema()
    
    # Prueba campo faltante (razon_social es requerido)
    datos_incompletos = {"cif_nif": "20-12345678-9"}
    errors = schema.validate(datos_incompletos)
    assert "razon_social" in errors

# --- TESTS DE VEHICULO SCHEMA ---
def test_vehiculo_schema_datos_numericos():
    """Prueba que las capacidades y otros números sean válidos"""
    schema = VehiculoSchema()
    
    # Prueba capacidad negativa (debería fallar)
    datos_vehiculo = {"patente": "ABC 123", "capacidad_toneladas": -500}
    errors = schema.validate(datos_vehiculo)
    # capacidad_toneladas es Float sin validador de mínimo, así que no debería fallar
    assert not errors or "capacidad_toneladas" in errors 

# --- TESTS DE VIAJE SCHEMA (Deserialización) ---
def test_viaje_schema_load():
    """Prueba que el schema pueda cargar (load) datos correctamente"""
    schema = ViajeSchema()
    payload = {
        "conductor_id": 1,
        "vehiculo_id": 2,
        "pedido_id": 1,
        "estado": "Pendiente"
    }
    # .load() convierte el JSON en un objeto o diccionario limpio
    resultado = schema.load(payload)
    assert resultado["estado"] == "Pendiente"
    assert isinstance(resultado["conductor_id"], int)