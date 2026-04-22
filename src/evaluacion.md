# Informe tecnico completo del proyecto "transporte"

Fecha de evaluacion: 2026-04-22

## 1) Resumen ejecutivo

El proyecto es una API Flask con SQLAlchemy, Flask-Migrate y JWT, pensada para gestionar operaciones de transporte de grano.
La arquitectura esta preparada para ejecutarse de dos formas:

- Modo local: `python run.py` + PostgreSQL en Docker (expuesto en `localhost:5433`).
- Modo Docker completo: `docker compose` con servicio `app` + `db` + `pgadmin`.

El enlace servidor-base de datos se hace por `DATABASE_URL`, cargada desde `.env` o desde variables inyectadas por Docker Compose.

## 2) Estructura real y funcion de cada pieza

```
/home/penascalf5/transporte/
├── run.py
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
│       ├── 8c5b4614cb00_init.py
│       └── 2d579c784a37_creacion_vehiculos_rutas_viajes.py
└── src/
    ├── app.py
    ├── config.py
    ├── database/db.py
    ├── routes/routes.py
    └── models/
        ├── actores.py
        ├── logistica_flota.py
        ├── operaciones.py
        └── __init__.py
```

## 3) Como se enlaza la logica (flujo interno)

Flujo de arranque principal:

1. `run.py` importa `create_app` desde `src/app.py`.
2. `create_app()` crea la app Flask.
3. `app.config.from_object(Config)` carga configuracion desde `src/config.py`.
4. `db.init_app(app)` inicializa SQLAlchemy.
5. `Migrate(app, db)` conecta Flask-Migrate con SQLAlchemy.
6. `JWTManager(app)` habilita JWT.
7. Dentro de `app.app_context()` se importan modelos y blueprint para registrar tablas y rutas.
8. Se registra el blueprint `routes_main`.
9. Se expone endpoint raiz `/`.

Flujo de request de API:

1. Llega una peticion HTTP.
2. Flask la enruta al blueprint `main` en `src/routes/routes.py`.
3. La funcion de ruta usa modelos SQLAlchemy para consultar o mutar datos.
4. SQLAlchemy ejecuta SQL contra PostgreSQL usando `psycopg2`.
5. La respuesta vuelve como JSON.

## 4) Conexion servidor <-> base de datos

La configuracion central esta en `src/config.py`:

- Se calcula la raiz del proyecto.
- Se carga `.env` con `load_dotenv(...)`.
- `SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")`.

### URL usada segun entorno

En local (`.env`):

`DATABASE_URL=postgresql://camiones:SLN3@localhost:5433/mydb`

En Docker Compose (servicio `app`):

`DATABASE_URL=postgresql://camiones:SLN3@db:5432/mydb`

Interpretacion:

- `localhost:5433` se usa desde la maquina host.
- `db:5432` se usa dentro de la red interna de Docker (nombre de servicio `db`).

## 5) Docker: imagenes, contenedores y red

### Imagen de aplicacion (Dockerfile)

- Base: `python:3.11-slim`
- Instala compilador y headers para `psycopg2`: `gcc libpq-dev`
- Instala dependencias desde `requirements.txt`
- Copia el proyecto a `/app`
- `CMD` por defecto: `gunicorn --bind 0.0.0.0:5000 src.app:create_app()`

### Orquestacion (docker-compose.yml)

Servicios:

- `app`
  - `build: .`
  - `command: python run.py` (esto sobrescribe el `CMD` de Gunicorn del Dockerfile)
  - Expone `5000:5000`
  - Depende de `db`
- `db`
  - Imagen `postgres:15-alpine`
  - Expone `5433:5432`
  - Variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `pgadmin`
  - Imagen `dpage/pgadmin4`
  - Expone `5050:80`
  - Depende de `db`

## 6) Como se guardan los datos (persistencia)

Estado actual real:

- En `docker-compose.yml` se declara `volumes: pgdata:`
- Pero el servicio `db` NO monta ese volumen en `/var/lib/postgresql/data`

Consecuencia:

- Si solo reinicias el contenedor, normalmente los datos siguen.
- Si eliminas/recreas contenedor (`docker compose down` + `up`), hay alto riesgo de perder datos.

Configuracion recomendada para persistencia real:

```yaml
db:
  ...
  volumes:
    - pgdata:/var/lib/postgresql/data
```

## 7) Modelo de datos y relaciones actuales

### Modulo `actores.py`

- `Usuario`
- `Cliente`
- `Conductor`

### Modulo `logistica_flota.py`

- `Vehiculo`
- `Ruta`
- `Viaje`
  - FK `conductor_id -> conductores.id`
  - FK `vehiculo_id -> vehiculos.id`
  - FK `ruta_id -> rutas.id`

### Modulo `operaciones.py`

- `Producto`
- `Pedido` (FK a `clientes`)
- `DetallePedido` (FK a `pedidos` y `productos`)
- `IncidenciaViaje` (FK a `viajes`)
- `InformeDescarga` (FK unico a `viajes`)
- `Factura` (FK unico a `pedidos`)

## 8) Migraciones y estado de esquema

Hay inconsistencias que debes conocer:

1. `2d579c784a37_creacion_vehiculos_rutas_viajes.py` referencia `down_revision='9894d6878205'`, pero ese archivo no existe en `migrations/versions/`.
2. Existe una migracion inicial `8c5b4614cb00_init.py` que crea `camiones`, pero luego otra migracion elimina `camiones` y crea `vehiculos`.
3. Las entidades de `operaciones.py` no aparecen en las migraciones actuales visibles.

Impacto:

- `flask db upgrade` podria fallar o dejar esquema incompleto segun el estado real de tu BD.

## 9) Rutas y servidor HTTP

Ruta registrada:

- `GET /camiones`

Observacion importante:

- La ruta fue corregida para consultar `Vehiculo.query.all()` y devolver la lista correctamente.

## 10) Como levantar todo el proyecto

### Opcion A: Todo en Docker

1. Construir y levantar:
```bash
docker compose up --build -d
```
2. Aplicar migraciones dentro del contenedor de app:
```bash
docker compose exec app flask --app run.py db upgrade
```
3. Verificar API:
```bash
curl http://localhost:5000/
```
4. Verificar pgAdmin:
   - URL: `http://localhost:5050`
   - Usuario: `admin@admin.com`
   - Password: `admin`

### Opcion B: App local + DB en Docker

1. Levantar solo base y pgAdmin:
```bash
docker compose up -d db pgadmin
```
2. Activar entorno local:
```bash
source myEnv/bin/activate
```
3. Aplicar migraciones:
```bash
flask --app run.py db upgrade
```
4. Levantar servidor:
```bash
python run.py
```

## 11) Como conectar el servidor a la base (paso a paso tecnico)

1. Define `DATABASE_URL` correcta para tu contexto (host o Docker interno).
2. `Config` lee esa variable y la asigna a SQLAlchemy.
3. `db.init_app(app)` crea el engine con ese DSN.
4. Al ejecutar una consulta del ORM, SQLAlchemy abre conexion via `psycopg2`.
5. PostgreSQL responde y SQLAlchemy transforma filas en objetos Python.

## 12) Diagnostico final del estado actual

Fortalezas:

- Arquitectura Flask modular bien encaminada.
- Separacion clara entre config, modelos, rutas y acceso a BD.
- Entorno Docker con `app`, `db` y `pgadmin`.
- Base para migraciones y autenticacion JWT ya integrada.

Riesgos tecnicos actuales:

1. Cadena de migraciones inconsistente (`down_revision` faltante).
2. Persistencia de PostgreSQL no montada en volumen activo.
3. Hay dos fabricas de app (`src/app.py` y `src/__init__.py`), lo que puede generar confusion si se usa la ruta incorrecta.

## 13) Recomendacion de orden de correccion

1. Reparar historial de migraciones para que `flask db upgrade` sea confiable.
2. Montar volumen `pgdata` en el servicio `db`.
3. Unificar punto de entrada/fabrica de app para evitar duplicidad de configuracion.

## 14) Guia paso a paso: conectar pgAdmin (Docker) y avanzar con tablas/CRUD

### 14.1 Levantar servicios necesarios

Si aun no estan levantados, ejecuta:

```bash
docker compose up -d db pgadmin
```

Si tambien quieres levantar la API en Docker:

```bash
docker compose up -d app
```

### 14.2 Entrar a pgAdmin

1. Abre en navegador: `http://localhost:5050`
2. Login con:
   - Email: `admin@admin.com`
   - Password: `admin`

### 14.3 Registrar el servidor PostgreSQL dentro de pgAdmin

1. En el panel izquierdo: click derecho en `Servers` -> `Register` -> `Server...`
2. Pestana `General`:
   - `Name`: `transporte-db` (o el nombre que quieras)
3. Pestana `Connection`:
   - `Host name/address`: `db`
   - `Port`: `5432`
   - `Maintenance database`: `mydb`
   - `Username`: `camiones`
   - `Password`: `SLN3`
   - Activa `Save password`
4. Click en `Save`.

Importante:
- Como pgAdmin corre en Docker Compose junto a PostgreSQL, el host correcto es `db` (nombre del servicio), no `localhost`.

### 14.4 Verificar que quedo conectado

1. Expande:
   - `Servers` -> `transporte-db` -> `Databases` -> `mydb` -> `Schemas` -> `public` -> `Tables`
2. Si no ves tablas aun, es normal: primero debes aplicar migraciones.

### 14.5 Crear tablas de forma correcta (recomendado)

Para este proyecto, lo correcto es crear tablas con Flask-Migrate/Alembic, no manualmente desde pgAdmin.

Si usas la app en Docker:

```bash
docker compose exec app flask --app run.py db migrate -m "sync modelos"
docker compose exec app flask --app run.py db upgrade
```

Si usas la app local (venv):

```bash
source myEnv/bin/activate
flask --app run.py db migrate -m "sync modelos"
flask --app run.py db upgrade
```

Luego en pgAdmin:
- Click derecho en `Tables` -> `Refresh` para ver las nuevas tablas.

### 14.6 Si quieres crear algo rapido en SQL desde pgAdmin

1. Selecciona `mydb`
2. Abre `Tools` -> `Query Tool`
3. Ejecuta SQL, por ejemplo:

```sql
SELECT current_database(), current_user;
```

Puedes crear tablas manuales, pero para mantener el proyecto ordenado y sin conflictos, usa migraciones para tablas del sistema principal.

### 14.7 Flujo recomendado para avanzar en CRUD

1. Definir/ajustar modelos en `src/models/`.
2. Generar migracion (`flask db migrate ...`).
3. Aplicar migracion (`flask db upgrade`).
4. Verificar tablas en pgAdmin.
5. Crear endpoints CRUD en `src/routes/routes.py`.
6. Probar endpoints (Postman/curl) y validar cambios en pgAdmin.

### 14.8 Errores tipicos y solucion rapida

- Error de conexion en pgAdmin:
  - Revisa que `db` y `pgadmin` esten arriba: `docker compose ps`
  - Verifica que usas `host=db` y `port=5432` dentro de pgAdmin
- Error al crear tablas con migraciones:
  - Revisa el historial de migraciones, porque en este proyecto hay inconsistencias de `down_revision`
- No aparecen tablas en pgAdmin:
  - Haz `Refresh` sobre `Tables`
  - Confirma que ejecutaste `flask db upgrade` contra la misma BD (`mydb`)

## 15) Solo abrir tu pgAdmin de Docker (pgadmin_ui)

Esta seccion es exactamente para este servicio:

```yaml
pgadmin:
  image: dpage/pgadmin4
  container_name: pgadmin_ui
  restart: always
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@admin.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
  depends_on:
    - db
```

Paso a paso:

1. Desde la raiz del proyecto (`/home/penascalf5/transporte`), levanta pgAdmin:
```bash
docker compose up -d pgadmin
```

2. Verifica que quedo levantado:
```bash
docker compose ps
```
Debes ver `pgadmin_ui` en estado `Up`.

3. Abre en el navegador:
`http://localhost:5050`

4. Inicia sesion en pgAdmin:
- Email: `admin@admin.com`
- Password: `admin`

5. Si no abre, revisa logs:
```bash
docker compose logs -f pgadmin
```

Nota:
- Aunque levantes solo `pgadmin`, por `depends_on` Docker Compose tambien levantara `db`.









