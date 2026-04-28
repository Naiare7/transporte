# Corrección de Errores en los CRUDs - Explicación Técnica

## Fecha: 28 de abril de 2026

## 1. Errores Identificados

### Error Original: RuntimeError de SECRET_KEY
```
RuntimeError: The session is unavailable because no secret key was set.
```

**Causa:** Flask necesita `SECRET_KEY` para usar sesiones (necesario para `flash()`).

### Errores Adicionales Detectados
1. Las operaciones CRUD no manejaban excepciones (si fallaba la base de datos, la aplicación crasheaba)
2. No había mensajes de error cuando una operación fallaba
3. Faltaba la opción de "volver al inicio" después de operaciones
4. Los mensajes flash no mostraban correctamente las categorías de error

## 2. Correcciones Realizadas

### 2.1 Configuración de SECRET_KEY (Arreglo del RuntimeError)

**Archivo modificado:** `src/config.py`

```python
class Config:
    # Clave para sesiones de Flask (AÑADIDO)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey_supersecretkey_123456')
    
    # Clave para JWT tokens (ya existía)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey_supersecretkey_123456')
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**Explicación:**
- `SECRET_KEY`: Firmar cookies de sesión de Flask, CSRF, flash messages
- `JWT_SECRET_KEY`: Firmar tokens JWT (independiente de SECRET_KEY)
- Se carga desde `.env` o usa valor por defecto

### 2.2 Manejo de Excepciones en CRUDs

**Archivo modificado:** `src/web/views.py`

Se añadió bloque `try-except` en todas las rutas:

```python
# EJEMPLO: clientes_new()
@web_bp.route("/clientes/new", methods=["GET", "POST"])
def clientes_new():
    if request.method == "POST":
        try:
            data = {
                "razon_social": request.form.get("razon_social"),
                "cif_nif": request.form.get("cif_nif"),
                "telefono": request.form.get("telefono"),
                "direccion": request.form.get("direccion")
            }
            ActoresService.create_cliente(data)
            flash("Cliente creado exitosamente", "success")
            return redirect(url_for("web.clientes_list"))
        except Exception as e:
            flash(f"Error al crear cliente: {str(e)}", "error")
            return render_template("clientes/form.html", cliente=None)
    return render_template("clientes/form.html", cliente=None)
```

**Qué hace este código:**
1. Intenta ejecutar la operación de base de datos
2. Si tiene éxito: muestra mensaje "success" y redirige
3. Si falla: captura la excepción, muestra mensaje "error" con detalles y vuelve al formulario

**Rutas corregidas:**
- `/clientes` (listar)
- `/clientes/new` (crear)
- `/clientes/<id>/edit` (editar)
- `/clientes/<id>/delete` (eliminar)
- `/vehiculos` (listar)
- `/vehiculos/new` (crear)
- `/vehiculos/<id>/edit` (editar)
- `/vehiculos/<id>/delete` (eliminar)
- `/pedidos` (listar)
- `/pedidos/new` (crear)
- `/pedidos/<id>/edit` (editar)
- `/pedidos/<id>/delete` (eliminar)

### 2.3 Mensajes de Éxito y Error

**Categorías de mensajes implementadas:**

| Categoría | Uso | Color |
|-----------|-----|-------|
| `success` | Operación exitosa (crear, editar, eliminar) | Verde |
| `error` | Error en la operación (base de datos, validación) | Rojo |

**Ejemplo de mensajes:**
```python
# Éxito
flash("Cliente creado exitosamente", "success")
flash("Vehículo actualizado exitosamente", "success")
flash("Pedido eliminado exitosamente", "success")

# Error
flash(f"Error al crear cliente: {str(e)}", "error")
flash(f"Error al listar vehículos: {str(e)}", "error")
```

### 2.4 Opción de Volver al Inicio

**Archivo modificado:** `src/templates/partials/_messages.html`

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="flash-messages">
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
        </div>
    {% endif %}
{% endwith %}

{% if request.endpoint != 'web.index' %}
<div class="back-to-home">
    <a href="{{ url_for('web.index') }}" class="btn">← Volver al inicio</a>
</div>
{% endif %}
```

**Explicación:**
- Muestra todos los mensajes flash con su categoría correspondiente
- Si no estamos en la página de inicio, muestra el botón "Volver al inicio"
- Usa `request.endpoint` para identificar la ruta actual

### 2.5 Estilos CSS para Mensajes de Error

**Archivo modificado:** `src/static/css/app.css`

```css
.alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.back-to-home {
    margin-bottom: 20px;
}
```

## 3. Flujo de Error/Éxito Completo

### Ejemplo: Crear un Cliente

1. **Usuario hace clic en "Nuevo Cliente"**
   - GET `/clientes/new` → Muestra formulario

2. **Usuario envía formulario con datos válidos**
   - POST `/clientes/new`
   - `ActoresService.create_cliente(data)` → ÉXITO
   - `flash("Cliente creado exitosamente", "success")`
   - Redirige a `/clientes`
   - Usuario ve mensaje verde: "Cliente creado exitosamente"
   - Ve botón "← Volver al inicio"

3. **Usuario envía formulario con datos inválidos (ej: CIF duplicado)**
   - POST `/clientes/new`
   - `ActoresService.create_cliente(data)` → ERROR (excepción de base de datos)
   - `flash(f"Error al crear cliente: {str(e)}", "error")`
   - Vuelve al formulario (no redirige)
   - Usuario ve mensaje rojo: "Error al crear cliente: [detalle del error]"
   - Ve botón "← Volver al inicio"

4. **Usuario hace clic en "Volver al inicio"**
   - Navega a `/`
   - Muestra página de inicio con tarjetas de módulos

## 4. Estructura de Archivos Modificados

```
src/
├── config.py                          # ← Añadido SECRET_KEY
├── web/
│   └── views.py                      # ← Añadido try-except en todas las rutas
├── templates/
│   └── partials/
│       └── _messages.html            # ← Añadido botón volver al inicio
└── static/
    └── css/
        └── app.css                   # ← Añadido estilos .alert-error y .back-to-home
```

## 5. Cómo Probar las Correcciones

### Paso 1: Reconstruir contenedores Docker
```bash
cd /home/penascalf5/transporte
docker-compose up -d --build
```

### Paso 2: Probar operación exitosa
1. Ir a `http://localhost:5000/clientes`
2. Hacer clic en "Nuevo Cliente"
3. Llenar formulario y guardar
4. Ver mensaje verde: "Cliente creado exitosamente"
5. Ver botón "← Volver al inicio"

### Paso 3: Probar manejo de errores
1. Ir a `http://localhost:5000/clientes/new`
2. Intentar crear cliente con CIF/NIF que ya exista
3. Ver mensaje rojo de error con detalles
4. Ver botón "← Volver al inicio"

### Paso 4: Verificar que SECRET_KEY funciona
- Si no aparece el error `RuntimeError: The session is unavailable...`
- Los mensajes flash se muestran correctamente
- La sesión funciona sin errores

## 6. Resumen de Cambios

| Problema | Solución | Archivo(s) |
|----------|----------|------------|
| RuntimeError SECRET_KEY | Añadir SECRET_KEY a Config | `src/config.py` |
| CRUDs sin manejo de errores | Bloques try-except en todas las rutas | `src/web/views.py` |
| Sin mensajes de error | Flash con categoría "error" | `src/web/views.py` |
| Sin botón volver inicio | Enlace en _messages.html | `src/templates/partials/_messages.html` |
| Sin estilo para errores | CSS para .alert-error | `src/static/css/app.css` |

## 7. Notas Importantes

1. **SECRET_KEY en producción:** Cambiar el valor por uno seguro y único
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Variables de entorno:** Se puede añadir `SECRET_KEY` al archivo `.env`:
   ```env
   SECRET_KEY=valor_seguro_y_secreto_aqui
   ```

3. **Manejo de errores:** Se capturan todas las excepciones con `Exception as e`, lo cual es útil para desarrollo. En producción, se podrían manejar tipos de errores específicos (ej: `IntegrityError` para duplicados).

4. **Experiencia de usuario:** Ahora ante cualquier error, el usuario ve un mensaje descriptivo y tiene la opción de volver al inicio o reintentar la operación.
