# Plan Maestro Backend - Proyecto Transporte

Fecha: 2026-04-23

## 1) Objetivo del documento

Este documento define la informacion minima y el orden de trabajo para que una IA (o cualquier dev) pueda:

1. Entender como esta organizado el proyecto.
2. Implementar CRUDs completos por entidad.
3. Crear peticiones HTTP consistentes.
4. Relacionar correctamente las entidades para un backend funcional.
5. Avanzar sin romper la arquitectura actual.

## 2) Estado real del proyecto (confirmado)

Stack actual:
- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.1.0
- Flask-JWT-Extended 4.7.1
- PostgreSQL 15 (Docker)
- Alembic (migraciones)

Entrypoint real en uso:
- `run.py` -> `src/app.py:create_app`

Configuracion de BD:
- `src/config.py` carga `.env`
- `SQLALCHEMY_DATABASE_URI = DATABASE_URL`

Variables clave:
- `DATABASE_URL`
- `JWT_SECRET_KEY`

## 3) Estructura de carpetas actual

```text
/home/penascalf5/transporte/
├── run.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
│       ├── 8c5b4614cb00_init.py
│       └── 2d579c784a37_creacion_vehiculos_rutas_viajes.py
├── historia/
│   ├── arranque.md
│   ├── evaluacion.md
│   └── plan.md
└── src/
    ├── app.py
    ├── config.py
    ├── __init__.py
    ├── database/
    │   └── db.py
    ├── models/
    │   ├── __init__.py
    │   ├── actores.py
    │   ├── logistica_flota.py
    │   └── operaciones.py
    └── routes/
        ├── __init__.py
        └── routes.py
```

## 4) Orden para leer y entender el proyecto (instruccion para IA)

Orden obligatorio de lectura:

1. `run.py` (entrada de ejecucion)
2. `src/app.py` (factory, extensiones, blueprint)
3. `src/config.py` (carga de entorno)
4. `src/database/db.py` (instancia de SQLAlchemy)
5. `src/models/*.py` (entidades y relaciones)
6. `src/routes/routes.py` (endpoints actuales)
7. `migrations/versions/*.py` (estado real de esquema)
8. `docker-compose.yml` (servicios y puertos)

Regla:
- No tomar `src/__init__.py` como punto de entrada principal.
- El punto de entrada correcto hoy es `src/app.py`.

## 5) Entidades y relaciones del dominio

### 5.1 Entidades actuales

`src/models/actores.py`
- `Usuario`
- `Cliente`
- `Conductor`

`src/models/logistica_flota.py`
- `Vehiculo`
- `Ruta`
- `Viaje`

`src/models/operaciones.py`
- `Producto`
- `Pedido`
- `DetallePedido`
- `IncidenciaViaje`
- `InformeDescarga`
- `Factura`

### 5.2 Relaciones (mapa funcional)

1. `Cliente 1 -> N Pedido`
2. `Pedido 1 -> N DetallePedido`
3. `Producto 1 -> N DetallePedido`
4. `Conductor 1 -> N Viaje`
5. `Vehiculo 1 -> N Viaje`
6. `Ruta 1 -> N Viaje`
7. `Viaje 1 -> N IncidenciaViaje`
8. `Viaje 1 -> 1 InformeDescarga` (unico por viaje)
9. `Pedido 1 -> 1 Factura` (unica por pedido)

### 5.3 Orden funcional del negocio

Flujo recomendado de uso:

1. Crear catalogos base: `Cliente`, `Conductor`, `Vehiculo`, `Ruta`, `Producto`.
2. Crear `Pedido` para un `Cliente`.
3. Agregar lineas en `DetallePedido`.
4. Crear `Viaje` usando `Conductor + Vehiculo + Ruta`.
5. Registrar `IncidenciaViaje` (si aplica).
6. Registrar `InformeDescarga` al finalizar viaje.
7. Emitir `Factura` desde `Pedido`.

## 6) Orden recomendado para implementar CRUDs

### Fase 0 - Base tecnica (bloqueante)

1. Validar arranque local y Docker.
2. Verificar migraciones aplicables:
   - `flask --app run.py db upgrade`
3. Si faltan tablas de `operaciones.py`, generar nueva migracion:
   - `flask --app run.py db migrate -m "agrega tablas operativas"`
   - `flask --app run.py db upgrade`
4. Definir formato de respuesta JSON comun:
   - `{"ok": true|false, "data": ..., "error": ...}`

### Fase 1 - CRUDs de catalogo (primero)

CRUD completos para:

1. `Cliente`
2. `Conductor`
3. `Vehiculo`
4. `Ruta`
5. `Producto`

Endpoints por entidad:

- `POST   /api/<entidad>`
- `GET    /api/<entidad>`
- `GET    /api/<entidad>/<id>`
- `PUT    /api/<entidad>/<id>`
- `DELETE /api/<entidad>/<id>`

Validaciones minimas:

1. Unicos: `email`, `cif_nif`, `dni`, `patente`.
2. Campos requeridos no vacios.
3. Tipos numericos correctos (`Float`, `Integer`).

### Fase 2 - CRUDs transaccionales (despues de catalogos)

1. `Pedido`
2. `DetallePedido`
3. `Viaje`

Reglas:

1. No crear `Pedido` sin `cliente_id` existente.
2. No crear `DetallePedido` sin `pedido_id` y `producto_id` validos.
3. Calcular `subtotal = cantidad * tarifa_flete` en backend.
4. No crear `Viaje` sin `conductor_id`, `vehiculo_id`, `ruta_id` existentes.

### Fase 3 - Seguimiento y cierre operativo

1. `IncidenciaViaje`
2. `InformeDescarga`
3. `Factura`

Reglas:

1. `InformeDescarga` solo uno por `viaje_id` (unique).
2. `Factura` solo una por `pedido_id` (unique).
3. `Factura.total` calculado por suma de subtotales del pedido (o regla definida).

### Fase 4 - Autenticacion y permisos

1. CRUD de `Usuario` con hash de password.
2. Login con JWT.
3. Proteger rutas sensibles con `@jwt_required()`.
4. Permitir endpoints publicos solo donde tenga sentido (ejemplo salud API).

## 7) Estructura objetivo para escalar CRUDs

Mantener `models` como esta y crecer por capas:

```text
src/
├── app.py
├── config.py
├── database/
│   └── db.py
├── models/
│   └── ...
├── routes/
│   ├── __init__.py
│   ├── health.py
│   ├── actores.py
│   ├── logistica.py
│   └── operaciones.py
├── services/
│   ├── actores_service.py
│   ├── logistica_service.py
│   └── operaciones_service.py
└── schemas/
    ├── actores_schema.py
    ├── logistica_schema.py
    └── operaciones_schema.py
```

Responsabilidades:

1. `routes`: HTTP, parseo request/response, codigos de estado.
2. `services`: reglas de negocio y transacciones.
3. `models`: persistencia ORM.
4. `schemas` (o serializadores): validacion y normalizacion de payload.

## 8) Plan de endpoints por modulo

### 8.1 Actores

- `POST /api/usuarios`
- `POST /api/auth/login`
- `GET /api/clientes`
- `POST /api/clientes`
- `GET /api/conductores`
- `POST /api/conductores`

### 8.2 Logistica y flota

- `GET /api/vehiculos`
- `POST /api/vehiculos`
- `GET /api/rutas`
- `POST /api/rutas`
- `GET /api/viajes`
- `POST /api/viajes`
- `PATCH /api/viajes/<id>/estado`

### 8.3 Operaciones

- `GET /api/productos`
- `POST /api/productos`
- `GET /api/pedidos`
- `POST /api/pedidos`
- `GET /api/pedidos/<id>/detalles`
- `POST /api/detalles-pedido`
- `GET /api/viajes/<id>/incidencias`
- `POST /api/incidencias-viaje`
- `POST /api/informes-descarga`
- `POST /api/facturas`

## 9) Contratos base de peticiones (ejemplos)

### Crear cliente

```http
POST /api/clientes
Content-Type: application/json

{
  "razon_social": "Agro Norte SA",
  "cif_nif": "A12345678",
  "telefono": "+34 600000000",
  "direccion": "Sevilla"
}
```

### Crear pedido

```http
POST /api/pedidos
Content-Type: application/json

{
  "cliente_id": 1,
  "estado": "Pendiente",
  "observaciones_entrega": "Entregar antes de las 18:00"
}
```

### Crear detalle de pedido

```http
POST /api/detalles-pedido
Content-Type: application/json

{
  "pedido_id": 1,
  "producto_id": 2,
  "cantidad": 20,
  "unidad_medida": "Toneladas",
  "tarifa_flete": 45.5,
  "requerimientos_especiales": "Sin humedad"
}
```

### Crear viaje

```http
POST /api/viajes
Content-Type: application/json

{
  "conductor_id": 1,
  "vehiculo_id": 1,
  "ruta_id": 3,
  "estado": "Programado"
}
```

## 10) Checklist de calidad por cada CRUD

Checklist minimo:

1. `POST` crea y devuelve `201`.
2. `GET` lista devuelve `200`.
3. `GET /<id>` devuelve `404` si no existe.
4. `PUT/PATCH` valida datos y devuelve `200`.
5. `DELETE` devuelve `204` o `404`.
6. Errores devuelven JSON consistente.
7. Cada endpoint tiene prueba feliz y prueba de error.

## 11) Pruebas de peticiones (orden recomendado)

1. Probar salud API (`GET /` o `GET /health`).
2. Cargar catalogos (`clientes`, `conductores`, `vehiculos`, `rutas`, `productos`).
3. Crear `pedido`.
4. Crear `detalle_pedido`.
5. Crear `viaje`.
6. Registrar `incidencia` e `informe_descarga`.
7. Generar `factura`.
8. Validar lecturas cruzadas:
   - `GET /api/pedidos/<id>`
   - `GET /api/viajes/<id>`
   - `GET /api/clientes/<id>/pedidos` (si se expone)

## 12) Comandos operativos utiles

Arranque Docker:

```bash
docker compose up -d --build
```

Aplicar migraciones:

```bash
flask --app run.py db upgrade
```

Crear migracion:

```bash
flask --app run.py db migrate -m "descripcion_cambio"
```

Revisar tablas:

```bash
docker exec -it postgres_db psql -U camiones -d mydb -c "\dt"
```

## 13) Riesgos actuales a considerar antes de programar mas CRUDs

1. `src/__init__.py` tiene una factory distinta y no debe usarse como referencia principal.
2. Hoy solo existe endpoint funcional `GET /camiones`.
3. El servicio `db` en `docker-compose.yml` declara volumen `pgdata` pero no lo monta en `/var/lib/postgresql/data`.
4. Entidades de `operaciones.py` pueden requerir migracion adicional si no estan en BD.

## 14) Prompt base para delegar a otra IA (copiar y usar)

```text
Trabaja sobre /home/penascalf5/transporte.

Objetivo:
Implementar CRUDs REST para todas las entidades del proyecto Transporte, respetando la estructura actual Flask + SQLAlchemy.

Orden obligatorio:
1) Leer run.py, src/app.py, src/config.py, src/database/db.py.
2) Leer src/models/*.py y mapear relaciones.
3) Revisar migraciones en migrations/versions.
4) Crear/ajustar rutas por modulo en src/routes.
5) Implementar validaciones y serializacion JSON.
6) Ejecutar migraciones faltantes.
7) Probar endpoints en orden: catalogos -> pedidos/detalles -> viajes -> incidencias/informes -> facturas.

Reglas:
- Mantener compatibilidad con Flask-Migrate.
- No romper create_app en src/app.py.
- Devolver codigos HTTP correctos y JSON consistente.
- Documentar cada endpoint creado.
```

## 15) Resultado esperado al finalizar este plan

Backend con:

1. CRUD completo para todas las entidades.
2. Relaciones funcionando con integridad referencial.
3. Flujo operativo completo: cliente -> pedido -> viaje -> descarga -> factura.
4. Endpoints listos para consumir desde frontend o Postman.
