# Proyecto Transporte - Evaluación Técnica

## 1. Estructura del Proyecto

```
/home/penascalf5/transporte/
├── .env                    # Variables de entorno (credenciales BD)
├── docker-compose.yml      # Contenedores Docker (PostgreSQL + pgAdmin)
├── run.py                 # Punto de entrada del servidor Flask
├── requirements.txt       # Dependencias Python
├── src/
│   ├── app.py             # Configuración principal de Flask
│   ├── config.py          # Carga de configuración desde .env
│   ├── database/
│   │   └── db.py          # Inicialización de SQLAlchemy
│   ├── models/
│   │   ├── vehiculos.py   # Modelo Camion (tabla camiones)
│   │   └── actores.py     # Otros modelos
│   └── routes/
│       └── routes.py     # Endpoints de la API
└── migrations/
    └── versions/
        └── ...           # Migraciones Alembic
```

## 2. Tecnologías Utilizadas

| Tecnología | Propósito | Versión |
|------------|----------|---------|
| **Flask** | Framework web/backend | 3.1.3 |
| **Flask-SQLAlchemy** | ORM para base de datos | 3.1.1 |
| **Flask-Migrate** | Gestor de migraciones (Alembic) | 4.1.0 |
| **Flask-JWT-Extended** | Autenticación con tokens JWT | 4.7.1 |
| **SQLAlchemy** | ORM base | 2.0.49 |
| **PostgreSQL** | Base de datos relacional | 15 (Docker) |
| **pgAdmin** | Interfaz visual para PostgreSQL | 4 (Docker) |
| **Python-dotenv** | Cargar variables desde .env | 1.2.2 |
| **psycopg2-binary** | Driver PostgreSQL para Python | 2.9.12 |

## 3. Base de Datos

### Tipo de Base de Datos
- **PostgreSQL 15** (imagen Alpine: `postgres:15-alpine`)
- Es una base de datos relacional (RDBMS) robusta y de código abierto

### Configuración (docker-compose.yml)
```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: postgres_db
    environment:
      POSTGRES_USER: usuario_admin
      POSTGRES_PASSWORD: password_seguro
      POSTGRES_DB: mi_base_datos
    ports:
      - "5433:5432"    # Puerto 5433 en host, 5432 en contenedor
    volumes:
      - pgdata:/var/lib/postgresql/data
```

### Credenciales de Conexión
- **Host**: `localhost`
- **Puerto**: `5433`
- **Usuario**: `usuario_admin`
- **Contraseña**: `password_seguro`
- **Base de datos**: `mi_base_datos`
- **URL completa**: `postgresql://usuario_admin:password_seguro@localhost:5433/mi_base_datos`

## 4. Cómo Conectar la Base de Datos

La conexión se configura automáticamente mediante:

1. **Archivo `.env`**: Contiene `DATABASE_URL` con las credenciales
2. **`src/config.py`**: Lee el `.env` con `load_dotenv()` y `os.getenv()`
3. **`src/app.py`**: Pasa la URI a SQLAlchemy via `app.config.from_object(Config)`
4. **`src/database/db.py`**: Inicializa `SQLAlchemy(app)` con la configuración

La app Flask usa **SQLAlchemy** como ORM que se conecta a PostgreSQL mediante el driver **psycopg2-binary**.

## 5. Cómo Levantar el Servidor y la Base de Datos

### Paso 1: Iniciar Docker (contenedores)
```bash
docker-compose up -d
```
Esto levanta:
- `postgres_db` (PostgreSQL en puerto 5433)
- `pgadmin_ui` (pgAdmin en puerto 5050)

El servicio `db` tiene `restart: always`, así que se reinicia automáticamente si falla.

### Paso 2: Activar el entorno virtual
```bash
source myEnv/bin/activate
```

### Paso 3: Ejecutar migraciones (crear tablas)
```bash
flask db upgrade
```
O también:
```bash
alembic upgrade head
```

### Paso 4: Iniciar el servidor Flask
```bash
python run.py
```
Servidor disponible en: `http://localhost:5000`

### ¿Se levanta automáticamente?
- **Docker**: Sí, con `restart: always` en docker-compose.yml
- **Flask**: No, debe iniciarse manualmente con `python run.py`
- Para automatización total, se podría usar **systemd**, **PM2**, o incluir Flask en docker-compose

### Acceso a pgAdmin (interfaz visual)
- URL: `http://localhost:5050`
- Email: `admin@admin.com`
- Contraseña: `admin`

## 6. Estado Actual del Proyecto

### Lo que YA está implementado:
- ✅ Estructura Flask completa
- ✅ Conexión a PostgreSQL configurada
- ✅ Modelo `Camion` creado (tabla `camiones`)
- ✅ Ruta `/camiones` (GET) funcionando
- ✅ Sistema de migraciones Alembic configurado
- ✅ Autenticación JWT preparada (JWTManager)

### Tablas existentes:
| Tabla | Estado | Descripción |
|-------|--------|-------------|
| `camiones` | ✅ Creada | Modelo en `src/models/vehiculos.py` |

## 7. Próximo Paso: Crear CRUDs

El proyecto **SÍ está listo** para comenzar a crear las tablas y CRUDS.

### sugerencia de siguiente paso:

1. **Completar el modelo `Camion`** - añadir más campos o relaciones
2. **Crear nuevos modelos** según necesidad, por ejemplo:
   - `Chofer` (conductores)
   - `Viaje` (registro de viajes)
   - `Cliente`
   - `Pedido`

3. **Crear CRUD completo** para cada entidad:
   - **C**reate: `POST /recurso`
   - **R**ead: `GET /recurso` y `GET /recurso/<id>`
   - **U**pdate: `PUT /recurso/<id>`
   - **D**elete: `DELETE /recurso/<id>`

4. **Añadir autenticación** con JWT a las rutas protegidas

### Ejemplo de siguiente paso recomendado:
```bash
# Crear nuevo modelo
flask db migrate -m "Crear tabla choferes"
flask db upgrade
```

Luego crear las rutas对应的es en `src/routes/routes.py`.