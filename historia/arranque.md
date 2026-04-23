# Arranque de servicios Docker - Transporte API

## Estructura del proyecto

```
transporte/
├── docker-compose.yml   # Define los servicios
├── Dockerfile           # Define la imagen de la app
├── src/                 # Código fuente
└── .env                 # Variables de entorno
```

## Puertos en uso

| Servicio | Contenedor | Puerto interno | Puerto externo | Descripción |
|----------|------------|----------------|-----------------|--------------|
| API Flask | transporte-app-1 | 5000 | 5000 | Servidor de la aplicación |
| PostgreSQL | postgres_db | 5432 | 5433 | Base de datos principal |
| pgAdmin | pgadmin_ui | 80 | 5050 | Interfaz web de PostgreSQL |

---

## Pasos detallados para levantar los servicios

### Paso 1: Verificar estado actual de Docker

```bash
docker ps -a
```

Esto muestra todos los contenedores (activos y detenidos).

### Paso 2: Ver las imágenes Docker disponibles

```bash
docker images
```

Imágenes usadas en este proyecto:
- `transporte-app` - Imagen construida localmente (Dockerfile)
- `postgres:15-alpine` - Base de datos PostgreSQL
- `dpage/pgadmin4` - Interfaz pgAdmin4

### Paso 3: Detener contenedores existentes (limpieza)

```bash
docker compose down -v
```

- `down` = detiene los contenedores
- `-v` = elimina los volúmenes (datos de la base de datos)

### Paso 4: Construir y levantar TODOS los servicios

```bash
docker compose up -d --build
```

- `up` = levanta los servicios definidos en docker-compose.yml
- `-d` = modo "detached" (en segundo plano)
- `--build` = reconstruye la imagen de la app antes de iniciar

### Paso 5: Verificar que todos los servicios estén corriendo

```bash
docker ps
```

Salida esperada:
```
CONTAINER ID   IMAGE                STATUS          PORTS
postgres_db     postgres:15-alpine   Up              0.0.0.0:5433->5432/tcp
pgadmin_ui      dpage/pgadmin4       Up              0.0.0.0:5050->80/tcp
transporte-app- transporte-app       Up              0.0.0.0:5000->5000/tcp
```

### Paso 6: Probar que la API responde

```bash
curl http://localhost:5000/
```

Debe responder: `¡Servidor de Transporte con estructura perfecta funcionando!`

---

## Servicios individuales

### Levantar solo la base de datos PostgreSQL

```bash
docker compose up -d db
```

### Levantar solo pgAdmin (interfaz de BD)

```bash
docker compose up -d pgadmin
```

### Levantar solo la API

```bash
docker compose up -d app
```

### Levantar la API con logs visibles (modo desarrollo)

```bash
docker compose up app
```

---

## Credenciales de acceso

### pgAdmin (Interfaz web de PostgreSQL)
- URL: http://localhost:5050
- Email: `admin@admin.com`
- Password: `admin`

### PostgreSQL (Base de datos)
- Host: `localhost`
- Puerto: `5433`
- User: `camiones`
- Password: `SLN3`
- Database: `mydb`

### API Flask
- URL: http://localhost:5000
- Puerto interno del contenedor: 5000

---

## Comandos útiles

```bash
# Ver logs de un servicio específico
docker compose logs db
docker compose logs app
docker compose logs pgadmin

# Ver logs en tiempo real
docker compose logs -f app

# Reiniciar un servicio
docker compose restart db

# Entrar al shell de PostgreSQL
docker exec -it postgres_db psql -U camiones -d mydb

# Entrar al shell del contenedor de la app
docker exec -it transporte-app-1 /bin/sh

# Listar bases de datos en PostgreSQL
docker exec -it postgres_db psql -U camiones -d mydb -c "\l"

# Listar tablas en la base de datos
docker exec -it postgres_db psql -U camiones -d mydb -c "\dt"

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

---

## Levantar desarrollo local (sin Docker)

Si quieres correr la app localmente (fuera de Docker):

### Opción 1: Usar el entorno virtual

```bash
source myEnv/bin/activate
python run.py
```

**Nota:** El puerto 5000 debe estar libre (detener el contenedor Docker primero).

### Opción 2: Cambiar puerto en desarrollo local

Editar `run.py`:
```python
app.run(host="0.0.0.0", port=5001)  # Usar puerto 5001
```

Luego:
```bash
source myEnv/bin/activate
python run.py
```

Acceder a http://localhost:5001/

---

## Diagrama de comunicación

```
Usuario → :5000 (API Flask) → :5433 (PostgreSQL)
Usuario → :5050 (pgAdmin)  → :5432 (PostgreSQL interno)
```

- El usuario accede a la API por el puerto 5000
- La API se conecta a PostgreSQL por el puerto 5433 (externo) → 5432 (interno)
- pgAdmin accede a PostgreSQL por puerto interno 5432

---

## Ver las tablas de la base de datos

Hay varias formas de consultar las tablas:

### Opción 1: Usando psql (línea de comandos Docker)

```bash
docker exec -it postgres_db psql -U camiones -d mydb -c "\dt"
```

Esto lista todas las tablas.

Para describir una tabla específica:

```bash
docker exec -it postgres_db psql -U camiones -d mydb -c "\d usuarios"
docker exec -it postgres_db psql -U camiones -d mydb -c "\d vehiculos"
```

Comandos útiles de psql:
```bash
# Listar bases de datos
docker exec -it postgres_db psql -U camiones -d mydb -c "\l"

# Listar todas las tablas
docker exec -it postgres_db psql -U camiones -d mydb -c "\dt"

# Ver estructura de una tabla
docker exec -it postgres_db psql -U camiones -d mydb -c "\d nombre_tabla"

# Ver datos de una tabla
docker exec -it postgres_db psql -U camiones -d mydb -c "SELECT * FROM usuarios LIMIT 5;"

# Listar secuencias
docker exec -it postgres_db psql -U camiones -d mydb -c "\ds"

# Salir de psql
\q
```

### Opción 2: Usando pgAdmin (interfaz web)

1. Abrir http://localhost:5050
2. Login con: `admin@admin.com` / `admin`
3. En el panel izquierdo: **Servers** → **Servers** → **postgres_db** (o crear conexión)
4. Expandir **Databases** → **mydb** → **Schemas** → **public** → **Tables**
5. Doble clic en una tabla para ver los datos

Para crear el servidor en pgAdmin:
- Click derecho en **Servers** → **Create** → **Server**
- Name: `Transporte DB`
- Connection tab:
  - Host: `postgres_db`
  - Port: `5432`
  - Username: `camiones`
  - Password: `SLN3`
  - Database: `mydb`

### Opción 3: Usando la API directamente

```bash
curl http://localhost:5000/api/usuarios
curl http://localhost:5000/api/clientes
curl http://localhost:5000/api/vehiculos
```

---

## Modelos/Tablas de la base de datos

### Modelo: ACTORES (src/models/actores.py)

| Tabla | Descripción | Columnas principales |
|-------|-------------|---------------------|
| `usuarios` | Administradores del sistema | id, nombre, email, password_hash, fecha_creacion |
| `clientes` | Clientes que solicitan transporte | id, razon_social, cif_nif, telefono, direccion |
| `conductores` | Conductores de vehículos | id, nombre_completo, dni, carnet_conducir, telefono, disponible |

### Modelo: LOGÍSTICA Y FLOTA (src/models/logistica_flota.py)

| Tabla | Descripción | Columnas principales |
|-------|-------------|---------------------|
| `vehiculos` | Camiones de la flota | id, patente, capacidad_toneladas, tipo_grano, disponible |
| `rutas` | Trayectos estándar | id, origen, destino, distancia_km, tiempo_estimado_horas |
| `viajes` | Viajes programados/en curso | id, fecha_creacion, fecha_salida, estado, conductor_id, vehiculo_id, ruta_id |

### Modelo: OPERACIONES (src/models/operaciones.py)

| Tabla | Descripción | Columnas principales |
|-------|-------------|---------------------|
| `productos` | Catálogo de productos transportados | id, nombre, categoria, requiere_limpieza_especial |
| `pedidos` | Órdenes de transporte | id, fecha_pedido, estado, observaciones_entrega, cliente_id |
| `detalles_pedido` | Líneas de detalle del pedido | id, cantidad, unidad_medida, tarifa_flete, subtotal, pedido_id, producto_id |
| `incidencias_viaje` | Incidencias en ruta | id, fecha_incidencia, descripcion, gravedad, viaje_id |
| `informes_descarga` | Albarán de llegada | id, fecha_descarga, toneladas_entregadas_reales, porcentaje_humedad, viaje_id |
| `facturas` | Cobros finales | id, fecha_emision, total, pagada, pedido_id |

---

## Relaciones entre tablas

```
usuarios (1) ←→ (N) pedidos
clientes (1) ←→ (N) pedidos
pedidos (1) ←→ (N) detalles_pedido
pedidos (1) ←→ (1) facturas
productos (1) ←→ (N) detalles_pedido
conductores (1) ←→ (N) viajes
vehiculos (1) ←→ (N) viajes
rutas (1) ←→ (N) viajes
viajes (1) ←→ (N) incidencias_viaje
viajes (1) ←→ (1) informes_descarga
```

---

## Migraciones y tablas creadas

### Migraciones existentes

1. `8c5b4614cb00_init.py` - Migración inicial
2. `2d579c784a37_creacion_vehiculos_rutas_viajes.py` - Creación de vehículos, rutas y viajes

**Nota:** La migración `2d579c784a37` referencia a `down_revision='9894d6878205'` que no existe, pero la migración se aplicó correctamente.

### Tablas creadas en la base de datos

```sql
-- Migración: 8c5b4614cb00_init
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER NOT NULL, 
    nombre VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    password_hash VARCHAR(255) NOT NULL, 
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id)
)
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER NOT NULL, 
    razon_social VARCHAR(255) NOT NULL, 
    cif_nif VARCHAR(255), 
    telefono VARCHAR(255), 
    direccion VARCHAR(255), 
    PRIMARY KEY (id)
)
CREATE TABLE IF NOT EXISTS conductores (
    id INTEGER NOT NULL, 
    nombre_completo VARCHAR(255) NOT NULL, 
    dni VARCHAR(255), 
    carnet_conducir VARCHAR(255), 
    telefono VARCHAR(255), 
    disponible BOOLEAN, 
    PRIMARY KEY (id)
)

-- Migración: 2d579c784a37_creacion_vehiculos_rutas_viajes
CREATE TABLE vehiculos (
    id SERIAL NOT NULL, 
    patente VARCHAR(10) NOT NULL, 
    capacidad_toneladas DOUBLE PRECISION, 
    tipo_grano TEXT, 
    disponible BOOLEAN, 
    PRIMARY KEY (id)
)
CREATE TABLE rutas (
    id SERIAL NOT NULL, 
    origen TEXT NOT NULL, 
    destino TEXT NOT NULL, 
    distancia_km DOUBLE PRECISION, 
    tiempo_estimado_horas DOUBLE PRECISION, 
    PRIMARY KEY (id)
)
CREATE TABLE viajes (
    id SERIAL NOT NULL, 
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE, 
    fecha_salida TIMESTAMP WITHOUT TIME ZONE, 
    estado VARCHAR(50), 
    conductor_id INTEGER, 
    vehiculo_id INTEGER, 
    ruta_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(conductor_id) REFERENCES conductores (id), 
    FOREIGN KEY(vehiculo_id) REFERENCES vehiculos (id), 
    FOREIGN KEY(ruta_id) REFERENCES rutas (id)
)

-- Migración: [MIGRACIÓN_INEXISTENTE]
-- Tabla: productos
CREATE TABLE productos (
    id INTEGER NOT NULL, 
    nombre VARCHAR(255) NOT NULL, 
    categoria VARCHAR(255), 
    requiere_limpieza_especial BOOLEAN, 
    PRIMARY KEY (id)
)

-- Migración: [MIGRACIÓN_INEXISTENTE]
-- Tabla: pedidos
CREATE TABLE pedidos (
    id INTEGER NOT NULL, 
    fecha_pedido TIMESTAMP WITHOUT TIME ZONE, 
    estado VARCHAR(50), 
    observaciones_entrega TEXT, 
    cliente_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(cliente_id) REFERENCES clientes (id)
)

-- Migración: [MIGRACIÓN_INEXISTENTE]
-- Tabla: detalles_pedido
CREATE TABLE detalles_pedido (
    id INTEGER NOT NULL, 
    cantidad INTEGER, 
    unidad_medida VARCHAR(50), 
    tarifa_flete INTEGER, 
    subtotal INTEGER, 
    pedido_id INTEGER, 
    producto_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(pedido_id) REFERENCES pedidos (id), 
    FOREIGN KEY(producto_id) REFERENCES productos (id)
)

-- Migración: [MIGRACIÓN_INEXISTENTE]
-- Tabla: incidencias_viaje
CREATE TABLE incidencias_viaje (
    id INTEGER NOT NULL, 
    fecha_incidencia TIMESTAMP WITHOUT TIME ZONE, 
    descripcion TEXT, 
    gravedad VARCHAR(50), 
    viaje_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(viaje_id) REFERENCES viajes (id)
)

-- Migración: [MIGRACIÓN_INEXISTENTE]
-- Tabla: informes_descarga
CREATE TABLE informes_descarga (
    id INTEGER NOT NULL, 
    fecha_descarga TIMESTAMP WITHOUT TIME ZONE, 
    toneladas_entregadas_reales INTEGER, 
    porcentaje_humedad INTEGER, 
    viaje_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(viaje_id) REFERENCES viajes (id)
)

-- Migración: [MIGRACIÓN_INEXISTENTE]
-- Tabla: facturas
CREATE TABLE facturas (
    id INTEGER NOT NULL, 
    fecha_emision TIMESTAMP WITHOUT TIME ZONE, 
    total INTEGER, 
    pagada BOOLEAN, 
    pedido_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(pedido_id) REFERENCES pedidos (id)
)
```

**Nota:** Las migraciones para `productos`, `pedidos`, `detalles_pedido`, `incidencias_viaje`, `informes_descarga` y `facturas` no se encuentran en el sistema de archivos, por lo que no se pueden ejecutar. Se deben crear los archivos correspondientes y generar las migraciones.