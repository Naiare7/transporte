from src.app import create_app
from src.database.db import db
from werkzeug.security import generate_password_hash
from datetime import datetime

# Importar todas las entidades (10 Modelos)
from src.models.actores import Usuario, Cliente, Conductor
from src.models.logistica_flota import Vehiculo, Ruta, Viaje
from src.models.seguimiento import Pedido, DetallePedido, IncidenciaViaje, Factura

app = create_app()

def seed_database():
    with app.app_context():
        print("Iniciando repoblación de la Base de Datos...")

        try:
            # 0. Limpiar la base de datos (En orden inverso a las dependencias)
            print("Limpiando datos antiguos...")
            db.session.query(Factura).delete()
            db.session.query(IncidenciaViaje).delete()
            db.session.query(DetallePedido).delete()
            db.session.query(Viaje).delete()
            db.session.query(Pedido).delete()
            db.session.query(Vehiculo).delete()
            db.session.query(Ruta).delete()
            db.session.query(Conductor).delete()
            db.session.query(Cliente).delete()
            db.session.query(Usuario).delete()
            db.session.commit()

            # 1. Crear Usuario Administrador
            print("Creando Usuario...")
            usuario1 = Usuario(
                nombre="Admin",
                email="admin@transporte.com",
                password_hash=generate_password_hash("admin123")
            )
            db.session.add(usuario1)
            db.session.commit()

            # 2. Crear Cliente
            print("Creando Cliente...")
            cliente1 = Cliente(
                razon_social="Agrícola del Norte S.L.",
                cif_nif="B12345678",
                telefono="600123456",
                direccion="Polígono Sur, Nave 4"
            )
            db.session.add(cliente1)
            db.session.commit()

            # 3. Crear Conductor
            print("Creando Conductor...")
            conductor1 = Conductor(
                nombre_completo="Juan Pérez",
                dni="12345678A",
                carnet_conducir="C+E",
                telefono="655987654",
                disponible=True
            )
            db.session.add(conductor1)
            db.session.commit()

            # 4. Crear Vehículo (Camión)
            print("Creando Vehículo...")
            vehiculo1 = Vehiculo(
                patente="1234-ABC",
                capacidad_toneladas=24.5,
                tipo_grano="Trigo",
                disponible=True
            )
            db.session.add(vehiculo1)
            db.session.commit()

            # 5. Crear Ruta
            print("Creando Ruta...")
            ruta1 = Ruta(
                origen="Sevilla",
                destino="Córdoba",
                distancia_km=140.5,
                tiempo_estimado_horas=2.0
            )
            db.session.add(ruta1)
            db.session.commit()

            # 6. Crear Pedido asociado al Cliente y al Usuario
            print("Creando Pedido...")
            pedido1 = Pedido(
                cliente_id=cliente1.id,
                usuario_id=usuario1.id,
                estado="Pendiente",
                observaciones_entrega="Cargar en muelle 3"
            )
            db.session.add(pedido1)
            db.session.commit()

            # 7. Crear Detalle del Pedido
            print("Creando Detalle de Pedido...")
            detalle1 = DetallePedido(
                descripcion_carga="Trigo limpio",
                cantidad=20.0,
                unidad_medida="Toneladas",
                tarifa_flete=15.5,
                subtotal=310.0,  # 20 * 15.5
                pedido_id=pedido1.id
            )
            db.session.add(detalle1)
            db.session.commit()

            # 8. Asignar el Viaje que une toda la logística
            print("Creando Viaje...")
            viaje1 = Viaje(
                conductor_id=conductor1.id,
                vehiculo_id=vehiculo1.id,
                ruta_id=ruta1.id,
                pedido_id=pedido1.id,
                usuario_id=usuario1.id,
                estado="Programado"
            )
            db.session.add(viaje1)
            db.session.commit()

            # 9. Crear una Incidencia de Vaje (para validar que funciona el modelo)
            print("Registrando Incidencia...")
            incidencia1 = IncidenciaViaje(
                viaje_id=viaje1.id,
                descripcion="Retraso por tráfico en autovía antes de la salida",
                gravedad="Leve"
            )
            db.session.add(incidencia1)
            db.session.commit()

            # 10. Crear Factura final del pedido
            print("Emitiendo Factura...")
            factura1 = Factura(
                 total=310.0,
                 pagada=False,
                 pedido_id=pedido1.id
            )
            db.session.add(factura1)
            db.session.commit()

            print("¡Éxito! Base de Datos poblada con las 10 entidades desde 0.")
        
        except Exception as e:
            db.session.rollback()
            print(f"Ocurrió un error poblando la base de datos: {e}")

if __name__ == "__main__":
    seed_database()
