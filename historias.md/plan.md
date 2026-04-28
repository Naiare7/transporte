# Plan paso a paso para construir plantillas Jinja simples y mantenibles

## 1. Objetivo
Construir una interfaz HTML con Jinja para probar CRUDs de forma rápida, con código sencillo y ordenado.

Este plan prioriza:
- simplicidad
- coherencia
- bajo acoplamiento
- buenas prácticas SOLID sin sobreingeniería

## 2. Alcance mínimo
Se crearán plantillas para tres módulos iniciales:
1. clientes
2. vehiculos
3. pedidos

Cada módulo tendrá:
- una vista de listado
- una vista de formulario (crear/editar)

Con eso se valida el flujo CRUD completo desde navegador.

## 3. Estructura final recomendada

```text
src/
├── web/
│   ├── __init__.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── partials/
│   │   ├── _navbar.html
│   │   ├── _messages.html
│   │   └── _table_actions.html
│   ├── clientes/
│   │   ├── list.html
│   │   └── form.html
│   ├── vehiculos/
│   │   ├── list.html
│   │   └── form.html
│   └── pedidos/
│       ├── list.html
│       └── form.html
└── static/
    └── css/
        └── app.css
```

## 4. Principios SOLID aplicados de manera sencilla
-------------------------------------------------------------------------------
1. SRP (responsabilidad única)
- `views.py` solo recibe request y decide qué renderizar.
- `services` manejan lógica de negocio y base de datos.
- `templates` solo muestran datos.

2. OCP (abierto/cerrado)
- `base.html` permite extender nuevas pantallas sin modificar el layout base.

3. LSP (sustitución)
- Se usa el mismo patrón de plantilla (`list.html`, `form.html`) en todos los módulos.

4. ISP (segregación)
- Plantillas parciales pequeñas (`_navbar`, `_messages`, `_table_actions`) para no mezclar todo en un archivo grande.

5. DIP (inversión de dependencias)
- Las vistas dependen de interfaces de servicio (métodos de `ActoresService`, `LogisticaService`, `TransaccionService`) y no de SQL directo.

## 5. Plan paso a paso de implementación

## Paso 1: Preparar blueprint web

Acciones:
1. Crear `src/web/views.py`.
2. Crear `Blueprint("web", __name__)`.
3. Registrar blueprint en `create_app()`.

Resultado esperado:
- La ruta `/` devuelve `index.html`.

## Paso 2: Crear layout base

Archivos:
- `templates/base.html`
- `templates/partials/_navbar.html`
- `templates/partials/_messages.html`

Contenido mínimo:
- estructura HTML5
- carga de `static/css/app.css`
- bloque `{% block content %}`
- inclusión de parciales con `{% include %}`

Resultado esperado:
- todas las páginas comparten estructura y navegación.

## Paso 3: Plantilla inicial de inicio

Archivo:
- `templates/index.html`

Acciones:
1. Extender `base.html`.
2. Mostrar accesos a clientes, vehiculos y pedidos.

Resultado esperado:
- home limpia y funcional.

## Paso 4: Construir módulo Clientes

Archivos:
- `templates/clientes/list.html`
- `templates/clientes/form.html`

Rutas en `views.py`:
- `GET /clientes`
- `GET/POST /clientes/new`
- `GET/POST /clientes/<id>/edit`
- `POST /clientes/<id>/delete`

Buenas prácticas:
- reutilizar `ActoresService`
- validar campos mínimos
- redireccionar a listado después de guardar

Resultado esperado:
- CRUD de clientes funcionando por HTML.

## Paso 5: Replicar patrón en Vehículos

Archivos:
- `templates/vehiculos/list.html`
- `templates/vehiculos/form.html`

Rutas:
- `GET /vehiculos`
- `GET/POST /vehiculos/new`
- `GET/POST /vehiculos/<id>/edit`
- `POST /vehiculos/<id>/delete`

Resultado esperado:
- CRUD de vehículos funcionando con la misma estructura.

## Paso 6: Replicar patrón en Pedidos

Archivos:
- `templates/pedidos/list.html`
- `templates/pedidos/form.html`

Rutas:
- `GET /pedidos`
- `GET/POST /pedidos/new`
- `GET/POST /pedidos/<id>/edit`
- `POST /pedidos/<id>/delete`

Resultado esperado:
- CRUD de pedidos funcionando con el mismo diseño.

## Paso 7: Añadir estilos mínimos

Archivo:
- `static/css/app.css`

Estilos mínimos:
- layout general
- tabla simple
- formulario limpio
- botones primario/secundario/eliminar

Resultado esperado:
- interfaz clara sin complejidad visual.

## Paso 8: Validación funcional final

Checklist:
1. `/` carga correctamente.
2. `/clientes`, `/vehiculos`, `/pedidos` listan datos.
3. Crear, editar y eliminar funciona en los tres módulos.
4. No hay consultas SQL directas en `views.py`.
5. API existente sigue funcionando en paralelo.

## 6. Reglas de código sencillo

1. Funciones cortas por ruta.
2. Nombres claros (`clientes_list`, `clientes_new`, `clientes_edit`).
3. Sin lógica de negocio en plantilla.
4. Sin duplicar bloques HTML: usar `extends` e `include`.
5. Si una plantilla crece demasiado, mover fragmentos a `partials/`.

## 7. Plantilla base de trabajo por cada módulo

Para cada entidad nueva, repetir exactamente esta secuencia:
1. Crear `list.html`.
2. Crear `form.html`.
3. Añadir 4 rutas (`list/new/edit/delete`).
4. Reutilizar service existente.
5. Probar manualmente el flujo CRUD.

Con este patrón se mantiene consistencia, simplicidad y cumplimiento práctico de SOLID.

---

# PROCESO DE EJECUCIÓN PASO A PASO

## Ejecución del Plan (Realizado)

### Paso 1: Preparar blueprint web ✅
1. Se creó el directorio `src/web/`
2. Se creó `src/web/__init__.py` (vacío, para hacer el directorio un paquete)
3. Se creó `src/web/views.py` con:
   - Blueprint "web" configurado con `template_folder="../templates"` y `static_folder="../static"`
   - Ruta `/` que renderiza `index.html`
   - Todas las rutas CRUD para clientes, vehículos y pedidos
4. Se modificó `src/app.py` para:
   - Importar `web_bp` desde `src.web.views`
   - Registrar el blueprint con `app.register_blueprint(web_bp)`

### Paso 2: Crear layout base ✅
1. Se creó `templates/base.html` con:
   - Estructura HTML5 básica
   - Carga de CSS: `url_for('static', filename='css/app.css')`
   - Bloque `{% block content %}` para contenido dinámico
   - Inclusión de parciales: `{% include 'partials/_navbar.html' %}` y `{% include 'partials/_messages.html' %}`

2. Se creó `templates/partials/_navbar.html` con:
   - Barra de navegación con enlaces a los tres módulos
   - Uso de `url_for('web.clientes_list')` para generar URLs

3. Se creó `templates/partials/_messages.html` con:
   - Manejo de mensajes flash: `get_flashed_messages(with_categories=true)`
   - Renderizado condicional de alertas

4. Se creó `templates/partials/_table_actions.html` con:
   - Botones de editar y eliminar reutilizables
   - Formulario para eliminar con confirmación JavaScript

### Paso 3: Plantilla inicial de inicio ✅
1. Se creó `templates/index.html` con:
   - Extiende `base.html`
   - Tarjetas de acceso a los tres módulos
   - Uso de `url_for` para enlaces dinámicos

### Paso 4: Construir módulo Clientes ✅
1. Se creó `templates/clientes/list.html` con:
   - Tabla que muestra todos los clientes
   - Bucle `{% for cliente in clientes %}` para iterar
   - Inclusión del parcial `_table_actions.html`
   - Manejo de caso vacío con `{% else %}`

2. Se creó `templates/clientes/form.html` con:
   - Formulario que sirve tanto para crear como editar
   - Campos pre-poblados si se edita: `value="{{ cliente.razon_social if cliente else '' }}"`
   - Uso de `url_for` para acciones del formulario

3. Se añadieron rutas en `views.py`:
   - `clientes_list()`: Obtiene todos los clientes usando `ActoresService.get_all_clientes()`
   - `clientes_new()`: Maneja GET (muestra formulario) y POST (crea cliente con `ActoresService.create_cliente(data)`)
   - `clientes_edit(id)`: Maneja GET (formulario con datos) y POST (actualiza con `ActoresService.update_cliente(cliente, data)`)
   - `clientes_delete(id)`: Elimina cliente con `ActoresService.delete_cliente(cliente)`

### Paso 5: Replicar patrón en Vehículos ✅
1. Se crearon `templates/vehiculos/list.html` y `form.html` siguiendo el mismo patrón
2. Se añadieron rutas en `views.py` usando `LogisticaService`
3. Formulario incluye checkbox para campo booleano `disponible`

### Paso 6: Replicar patrón en Pedidos ✅
1. Se crearon `templates/pedidos/list.html` y `form.html`
2. Se añadieron rutas en `views.py` usando `TransaccionService`
3. El formulario incluye un `<select>` para elegir cliente, poblado con `ActoresService.get_all_clientes()`
4. Se muestra el nombre del cliente en el listado usando `pedido.cliente.razon_social` (relación SQLAlchemy)

### Paso 7: Añadir estilos mínimos ✅
1. Se creó `static/css/app.css` con:
   - Estilos para navbar, tablas, formularios, botones
   - Layout responsive básico con CSS Grid para las tarjetas
   - Colores y espaciado consistente

---

# CÓMO FUNCIONAN LOS CRUDs CON JINJA

## Arquitectura y Conexión

```
Navegador (HTTP Request)
    ↓
Flask Blueprint (src/web/views.py)
    ↓
Service Layer (src/services/actores_service.py, etc.)
    ↓
SQLAlchemy Models (src/models/actores.py, etc.)
    ↓
PostgreSQL Database
    ↑
Jinja Templates (src/templates/)
    ↑
Flask render_template() devuelve HTML al navegador
```

## Flujo de un Request CRUD (Ejemplo: Clientes)

1. **Usuario accede a `/clientes`**
   - Flask ejecuta `clientes_list()` en `views.py`
   - La función llama a `ActoresService.get_all_clientes()`
   - El servicio hace `Cliente.query.all()` (SQLAlchemy)
   - `render_template("clientes/list.html", clientes=clientes)` pasa datos a la plantilla
   - Jinja renderiza el HTML con los datos y lo envía al navegador

2. **Usuario hace clic en "Nuevo Cliente"**
   - Navega a `/clientes/new` (método GET)
   - `clientes_new()` renderiza `clientes/form.html` sin datos (cliente=None)

3. **Usuario envía el formulario**
   - POST a `/clientes/new` con datos del formulario
   - `request.form.get("razon_social")` extrae datos
   - Se crea diccionario `data` y se pasa a `ActoresService.create_cliente(data)`
   - El servicio crea objeto `Cliente(**data)`, hace `db.session.add()` y `db.session.commit()`
   - Se muestra mensaje flash y redirige a `/clientes`

4. **Usuario edita un cliente**
   - GET a `/clientes/<id>/edit` muestra formulario con datos actuales
   - POST actualiza usando `ActoresService.update_cliente(cliente, data)`
   - El servicio usa `setattr()` para actualizar cada campo y hace commit

5. **Usuario elimina un cliente**
   - POST a `/clientes/<id>/delete` (desde formulario en la tabla)
   - `ActoresService.delete_cliente(cliente)` hace `db.session.delete()` y `commit()`

## Uso de Jinja en las Plantillas

### Herencia (Extends)
```html
{% extends "base.html" %}  <!-- Hereda estructura base -->
{% block content %}         <!-- Define contenido del bloque -->
    <!-- Contenido específico -->
{% endblock %}
```

### Inclusión (Include)
```html
{% include 'partials/_navbar.html' %}  <!-- Inserta contenido de otro archivo -->
```

### Bucles (For)
```html
{% for cliente in clientes %}
    <tr>
        <td>{{ cliente.id }}</td>  <!-- Muestra propiedad del objeto -->
    </tr>
{% else %}  <!-- Se ejecuta si la lista está vacía -->
    <tr><td>No hay datos</td></tr>
{% endfor %}
```

### Condicionales (If)
```html
{{ "Sí" if vehiculo.disponible else "No" }}  <!-- Operador ternario -->
```

### URL Building
```html
<a href="{{ url_for('web.clientes_list') }}">Clientes</a>  <!-- Genera URL desde nombre de ruta -->
```

### Manejo de Formularios
```html
<form method="POST">
    <input type="text" name="razon_social" value="{{ cliente.razon_social if cliente else '' }}">
    <!-- El valor se pre-pobla si se edita, sino está vacío -->
</form>
```

---

# QUÉ ES JINJA, CÓMO INSTALARLO Y CONFIGURARLO

## ¿Qué es Jinja?
Jinja es un motor de plantillas para Python. Permite generar HTML dinámico mezclando código Python (en estructuras especiales) con HTML estático. Flask lo usa por defecto para renderizar vistas.

**Características principales:**
- Sintaxis similar a Python (`{% %}` para lógica, `{{ }}` para mostrar variables)
- Herencia de plantillas (`extends`)
- Inclusión de fragmentos (`include`)
- Filtros para transformar datos (`{{ fecha|date }}`)
- Macros (como funciones)

## ¿Cómo se instala?
Jinja viene **incluido automáticamente con Flask**, no necesitas instalarlo por separado.

```bash
# Si usas Flask, Jinja ya está instalado
pip install Flask  # Esto instala Jinja automáticamente

# Verificar instalación
pip show Jinja2
```

En este proyecto, las dependencias están en `requirements.txt`:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
flask-migrate
flask-jwt-extended
python-dotenv
psycopg2-binary
gunicorn
```

## ¿Qué se necesita?
Para usar Jinja con Flask necesitas:
1. **Flask instalado** (Jinja viene con él)
2. **Estructura de directorios** (Flask busca templates en una carpeta `templates/` por defecto):
   ```
   proyecto/
   ├── app.py
   ├── templates/       ← Flask busca aquí automáticamente
   │   ├── base.html
   │   └── ...
   └── static/          ← Para CSS, JS, imágenes
       └── css/
   ```

## ¿Cómo se configura?
Flask configura Jinja automáticamente. Solo necesitas:

### 1. En tu aplicación Flask (`app.py`):
```python
from flask import Flask, render_template

app = Flask(__name__)  # Flask configura Jinja automáticamente

# O si usas Blueprints con carpetas personalizadas:
from flask import Blueprint
web_bp = Blueprint("web", __name__, 
                   template_folder="../templates",  # Donde están las plantillas
                   static_folder="../static")        # Donde están archivos estáticos
```

### 2. Para renderizar una plantilla:
```python
from flask import render_template

@app.route("/")
def index():
    datos = {"titulo": "Mi Página", "items": [1, 2, 3]}
    return render_template("index.html", **datos)  # Pasa variables a la plantilla
```

### 3. En la plantilla (`templates/index.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ titulo }}</title>  <!-- Muestra variable -->
</head>
<body>
    <ul>
    {% for item in items %}  <!-- Bucle -->
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

### 4. Configuración personalizada (opcional):
```python
app = Flask(__name__)

# Cambiar delimitadores (opcional)
app.jinja_env.variable_start_string = "[["
app.jinja_env.variable_end_string = "]]"

# Agregar funciones globales disponibles en todas las plantillas
def mi_funcion():
    return "Hola"
app.jinja_env.globals.update(mi_funcion=mi_funcion)

# Configurar filtros personalizados
def uppercase_filter(text):
    return text.upper()
app.jinja_env.filters['uppercase'] = uppercase_filter
```

## En este proyecto:
- **Blueprint configurado**: `web_bp = Blueprint("web", __name__, template_folder="../templates", static_folder="../static")`
- **Renderizado**: `return render_template("clientes/list.html", clientes=clientes)`
- **Uso de `url_for`**: Jinja usa `url_for('web.clientes_list')` para generar URLs desde el nombre de la función de la ruta

---

# CÓMO ARRANCAR EL PROYECTO Y USAR LOS CRUDs

## Requisitos Previos
- Docker y Docker Compose instalados
- Puerto 5000 (Flask), 5433 (PostgreSQL), 5050 (pgAdmin) disponibles

## Paso 1: Clonar/Acceder al Proyecto
```bash
cd /home/penascalf5/transporte
```

## Paso 2: Verificar Variables de Entorno
El archivo `.env` debe existir con:
```env
DATABASE_URL=postgresql://camiones:SLN3@db:5432/mydb
POSTGRES_DB=mydb
POSTGRES_USER=camiones
POSTGRES_PASSWORD=SLN3
JWT_SECRET_KEY=supersecretkey_supersecretkey_123456
DB_HOST=db
DB_PORT=5432
```

## Paso 3: Levantar los Servicios Docker
```bash
docker-compose up -d --build
```
Esto inicia:
- **app**: Servidor Flask en `http://localhost:5000`
- **db**: PostgreSQL en `localhost:5433`
- **pgadmin**: Interfaz pgAdmin en `http://localhost:5050`

## Paso 4: Verificar que los Servicios estén Corriendo
```bash
docker ps
```

## Paso 5: Ejecutar Migraciones (Primera vez)
```bash
docker exec -e FLASK_APP=run.py transporte_flask_app flask db upgrade
```

## Paso 6: Poblar la Base de Datos (Opcional)
```bash
docker exec -e FLASK_APP=run.py transporte_flask_app python seed.py
```

## Paso 7: Acceder a la Interfaz Web
Abrir en el navegador: `http://localhost:5000`

Verás la página de inicio con tres tarjetas:
- **Clientes**: Gestionar clientes
- **Vehículos**: Gestionar flota
- **Pedidos**: Gestionar pedidos

## Cómo Usar los CRUDs

### Gestión de Clientes
1. **Listar**: Click en "Clientes" → Ver tabla con todos los clientes
2. **Crear**: Click en "Nuevo Cliente" → Llenar formulario → "Guardar"
3. **Editar**: Click en "Editar" junto a un cliente → Modificar → "Guardar"
4. **Eliminar**: Click en "Eliminar" → Confirmar → Cliente eliminado

### Gestión de Vehículos
1. **Listar**: Click en "Vehículos" → Ver tabla con patente, capacidad, tipo de grano, disponibilidad
2. **Crear**: "Nuevo Vehículo" → Llenar patente, capacidad, tipo → "Guardar"
3. **Editar**: "Editar" → Modificar campos → "Guardar"
4. **Eliminar**: "Eliminar" → Confirmar

### Gestión de Pedidos
1. **Listar**: Click en "Pedidos" → Ver tabla con cliente, fecha, estado
2. **Crear**: "Nuevo Pedido" → Seleccionar cliente, estado, observaciones → "Guardar"
3. **Editar**: "Editar" → Cambiar estado o cliente → "Guardar"
4. **Eliminar**: "Eliminar" → Confirmar

## Comandos Útiles

### Ver logs de Flask:
```bash
docker logs transporte_flask_app -f
```

### Reiniciar servicios:
```bash
docker-compose restart app
```

### Reconstruir después de cambios:
```bash
docker-compose up -d --build
```

### Acceder a pgAdmin:
1. Ir a `http://localhost:5050`
2. Login: `admin@admin.com` / `admin`
3. Registrar servidor con Host: `db`, Port: `5432`, User: `camiones`, Password: `SLN3`

## Estructura de URLs para los CRUDs
- `/` → Página de inicio
- `/clientes` → Listar clientes
- `/clientes/new` → Formulario nuevo cliente (GET) / Crear (POST)
- `/clientes/<id>/edit` → Formulario editar cliente (GET) / Actualizar (POST)
- `/clientes/<id>/delete` → Eliminar cliente (POST)
- `/vehiculos` → Listar vehículos
- `/vehiculos/new` → Formulario nuevo vehículo
- `/vehiculos/<id>/edit` → Editar vehículo
- `/vehiculos/<id>/delete` → Eliminar vehículo
- `/pedidos` → Listar pedidos
- `/pedidos/new` → Formulario nuevo pedido
- `/pedidos/<id>/edit` → Editar pedido
- `/pedidos/<id>/delete` → Eliminar pedido

## Notas Importantes
1. Los CRUDs web funcionan en paralelo con la API REST existente
2. Los servicios (`ActoresService`, `LogisticaService`, `TransaccionService`) son compartidos por ambas interfaces
3. No hay SQL directo en las vistas, siguiendo el principio DIP de SOLID
4. La interfaz usa mensajes flash para confirmaciones de éxito/error
5. Los formularios validan campos requeridos en el lado del cliente (HTML5)
