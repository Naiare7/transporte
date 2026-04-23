# Arranque de servicios Docker - Transporte API

## Estructura del proyecto

```
transporte/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── run.py
├── src/
│   ├── app.py              # Factory de Flask
│   ├── config.py           # Configuración
│   ├── database/
│   │   └── db.py           # SQLAlchemy instance
│   ├── models/
│   │   ├── actores.py      # Usuario, Cliente, Conductor
│   │   ├── logistica_flota.py  # Vehiculo, Ruta, Viaje
│   │   └── operaciones.py  # Pedido, DetallePedido, etc.
│   ├── routes/
│   │   ├── actores.py      # CRUD Cliente, Conductor
│   │   ├── logistica.py    # CRUD Vehiculo, Ruta
│   │   ├── productos.py    # CRUD Producto
│   │   ├── transacciones.py # CRUD Pedido, DetallePedido, Viaje
│   │   ├── seguimiento.py  # CRUD Incidencia, Informe, Factura
│   │   └── auth.py         # Login JWT
│   ├── services/
│   │   └── *_service.py    # Lógica de negocio
│   └── schemas/
│       └── *_schema.py     # Validación con Marshmallow
└── migrations/
```

## Puertos en uso

| Servicio | Puerto externo | Descripción |
|----------|---------------|-------------|
| API Flask | 5000 | Servidor de la aplicación |
| PostgreSQL | 5433 | Base de datos |
| pgAdmin | 5050 | Interfaz web PostgreSQL |

---

## Pasos para levantar

```bash
# 1. Limpiar contenedores existentes
docker compose down -v

# 2. Construir y levantar todos los servicios
docker compose up -d --build

# 3. Verificar estado
docker ps

# 4. Verificar que la API responde
curl http://localhost:5000/
```

---

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login con email/password |
| POST | `/api/usuarios` | Crear usuario |
| GET | `/api/usuarios` | Listar usuarios |

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"password123"}'
```

**Crear usuario:**
```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Admin","email":"admin@test.com","password":"password123"}'
```

---

### Catálogos

#### Clientes (`/api/clientes`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/clientes` | Listar todos |
| GET | `/api/clientes/<id>` | Obtener uno |
| POST | `/api/clientes` | Crear |
| PUT | `/api/clientes/<id>` | Actualizar |
| DELETE | `/api/clientes/<id>` | Eliminar |

```bash
# Crear cliente
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"razon_social":"Agro Sevilla SL","cif_nif":"B12345678"}'
```

#### Conductores (`/api/conductores`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/conductores` | Listar todos |
| GET | `/api/conductores/<id>` | Obtener uno |
| POST | `/api/conductores` | Crear |
| PUT | `/api/conductores/<id>` | Actualizar |
| DELETE | `/api/conductores/<id>` | Eliminar |

```bash
# Crear conductor
curl -X POST http://localhost:5000/api/conductores \
  -H "Content-Type: application/json" \
  -d '{"nombre_completo":"Carlos García","dni":"56789012B","carnet_conducir":"C+E"}'
```

#### Vehículos (`/api/vehiculos`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/vehiculos` | Listar todos |
| GET | `/api/vehiculos/<id>` | Obtener uno |
| POST | `/api/vehiculos` | Crear |
| PUT | `/api/vehiculos/<id>` | Actualizar |
| DELETE | `/api/vehiculos/<id>` | Eliminar |

```bash
# Crear vehículo
curl -X POST http://localhost:5000/api/vehiculos \
  -H "Content-Type: application/json" \
  -d '{"patente":"ABC-001","capacidad_toneladas":25}'
```

#### Rutas (`/api/rutas`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/rutas` | Listar todos |
| GET | `/api/rutas/<id>` | Obtener uno |
| POST | `/api/rutas` | Crear |
| PUT | `/api/rutas/<id>` | Actualizar |
| DELETE | `/api/rutas/<id>` | Eliminar |

```bash
# Crear ruta
curl -X POST http://localhost:5000/api/rutas \
  -H "Content-Type: application/json" \
  -d '{"origen":"Madrid","destino":"Sevilla","distancia_km":530}'
```

#### Productos (`/api/productos`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/productos` | Listar todos |
| GET | `/api/productos/<id>` | Obtener uno |
| POST | `/api/productos` | Crear |
| PUT | `/api/productos/<id>` | Actualizar |
| DELETE | `/api/productos/<id>` | Eliminar |

```bash
# Crear producto
curl -X POST http://localhost:5000/api/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Trigo","categoria":"Grano"}'
```

---

### Transacciones

#### Pedidos (`/api/pedidos`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/pedidos` | Listar todos |
| GET | `/api/pedidos/<id>` | Obtener uno |
| POST | `/api/pedidos` | Crear |
| PUT | `/api/pedidos/<id>` | Actualizar |
| DELETE | `/api/pedidos/<id>` | Eliminar |
| GET | `/api/pedidos/<id>/detalles` | Ver detalles del pedido |

```bash
# Crear pedido
curl -X POST http://localhost:5000/api/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente_id":1}'
```

#### Detalles de Pedido (`/api/detalles-pedido`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/detalles-pedido` | Listar todos |
| POST | `/api/detalles-pedido` | Crear |
| PUT | `/api/detalles-pedido/<id>` | Actualizar |
| DELETE | `/api/detalles-pedido/<id>` | Eliminar |

```bash
# Crear detalle (calcula subtotal automático)
curl -X POST http://localhost:5000/api/detalles-pedido \
  -H "Content-Type: application/json" \
  -d '{"pedido_id":1,"producto_id":1,"cantidad":20,"tarifa_flete":50}'
```

#### Viajes (`/api/viajes`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/viajes` | Listar todos |
| GET | `/api/viajes/<id>` | Obtener uno |
| POST | `/api/viajes` | Crear |
| PUT | `/api/viajes/<id>` | Actualizar |
| DELETE | `/api/viajes/<id>` | Eliminar |
| PATCH | `/api/viajes/<id>/estado` | Cambiar estado |

```bash
# Crear viaje
curl -X POST http://localhost:5000/api/viajes \
  -H "Content-Type: application/json" \
  -d '{"conductor_id":1,"vehiculo_id":1,"ruta_id":1}'

# Cambiar estado
curl -X PATCH http://localhost:5000/api/viajes/1/estado \
  -H "Content-Type: application/json" \
  -d '{"estado":"En Tránsito"}'
```

---

### Seguimiento

#### Incidencias (`/api/incidencias-viaje`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/incidencias-viaje` | Listar todas |
| GET | `/api/incidencias-viaje/<id>` | Obtener una |
| POST | `/api/incidencias-viaje` | Crear |
| DELETE | `/api/incidencias-viaje/<id>` | Eliminar |
| GET | `/api/viajes/<id>/incidencias` | Incidencias de un viaje |

```bash
# Crear incidencia
curl -X POST http://localhost:5000/api/incidencias-viaje \
  -H "Content-Type: application/json" \
  -d '{"viaje_id":1,"descripcion":"Avería en rueda","gravedad":"Leve"}'
```

#### Informes de Descarga (`/api/informes-descarga`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/informes-descarga` | Listar todos |
| GET | `/api/informes-descarga/<id>` | Obtener uno |
| POST | `/api/informes-descarga` | Crear |
| PUT | `/api/informes-descarga/<id>` | Actualizar |
| GET | `/api/viajes/<id>/informe-descarga` | Informe de un viaje |

```bash
# Crear informe de descarga
curl -X POST http://localhost:5000/api/informes-descarga \
  -H "Content-Type: application/json" \
  -d '{"viaje_id":1,"toneladas_entregadas_reales":19.8,"porcentaje_humedad":11}'
```

#### Facturas (`/api/facturas`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/facturas` | Listar todas |
| GET | `/api/facturas/<id>` | Obtener una |
| POST | `/api/facturas` | Crear (calcula total automático) |
| PUT | `/api/facturas/<id>` | Actualizar |
| GET | `/api/pedidos/<id>/factura` | Factura de un pedido |

```bash
# Crear factura (calcula total desde detalles del pedido)
curl -X POST http://localhost:5000/api/facturas \
  -H "Content-Type: application/json" \
  -d '{"pedido_id":1}'
```

---

## Flujo completo del negocio

```
1. Crear catálogo base:
   - Cliente → Conductor → Vehículo → Ruta → Producto

2. Crear pedido:
   - Pedido (para un Cliente)
   - DetallePedido (líneas del pedido, calcula subtotal)

3. Crear viaje:
   - Viaje (conductor + vehículo + ruta)

4. Seguimiento:
   - IncidenciaViaje (si hay problemas)
   - InformeDescarga (al finalizar)

5. Facturación:
   - Factura (calcula total desde pedidos)
```

---

## Comandos útiles

```bash
# Ver logs de la API
docker compose logs -f app

# Ver logs de la base de datos
docker compose logs -f db

# Entrar a la base de datos
docker exec -it postgres_db psql -U camiones -d mydb

# Listar tablas
docker exec postgres_db psql -U camiones -d mydb -c "\dt"

# Ver datos de una tabla
docker exec postgres_db psql -U camiones -d mydb -c "SELECT * FROM clientes;"

# Limpiar todos los datos
docker exec postgres_db psql -U camiones -d mydb -c "TRUNCATE TABLE usuarios, clientes, conductores, vehiculos, rutas, productos, pedidos, detalles_pedido, viajes, incidencias_viaje, informes_descarga, facturas CASCADE;"
```

---

## Credenciales

| Servicio | Credenciales |
|----------|---------------|
| pgAdmin | admin@admin.com / admin |
| PostgreSQL | camiones / SLN3 |
| API | Puerto 5000 |