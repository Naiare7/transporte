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
