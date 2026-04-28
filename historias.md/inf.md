# Guía de Despliegue y Configuración del Proyecto Transporte

## Requisitos Previos
- Docker y Docker Compose instalados
- Git instalado
- Puerto 5000, 5433 y 5050 disponibles

## Paso 1: Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd transporte
```

## Paso 2: Configurar Variables de Entorno
Verificar que el archivo `.env` exista con el siguiente contenido:
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
Ejecutar el siguiente comando para construir las imágenes y levantar los contenedores:
```bash
docker-compose up -d --build
```

Esto levantará tres servicios:
- **app**: Servidor Flask en `http://localhost:5000`
- **db**: PostgreSQL en `localhost:5433` (dentro de Docker usa el puerto 5432)
- **pgadmin**: Interfaz pgAdmin en `http://localhost:5050`

## Paso 4: Verificar que los Servicios estén Corriendo
```bash
docker ps
```

Deberías ver tres contenedores: `transporte_flask_app`, `postgres_db`, y `pgadmin_ui`.

## Paso 5: Ejecutar las Migraciones de Base de Datos
Las migraciones ya se ejecutaron automáticamente en los pasos anteriores. Para verificar que las tablas se crearon:
```bash
docker exec postgres_db psql -U camiones -d mydb -c "\dt"
```

## Paso 6: Poblar la Base de Datos con Datos de Prueba (Opcional)
```bash
docker exec -e FLASK_APP=run.py transporte_flask_app python seed.py
```

## Paso 7: Configurar pgAdmin para ver las Tablas

1. Abrir en el navegador: `http://localhost:5050`
2. Iniciar sesión con:
   - Email: `admin@admin.com`
   - Contraseña: `admin`
3. En pgAdmin, hacer clic derecho en "Servers" > "Register" > "Server"
4. En la pestaña "General", poner nombre: `Transporte DB`
5. En la pestaña "Connection":
   - Host: `db` (nombre del servicio Docker, NO localhost)
   - Port: `5432`
   - Maintenance database: `mydb`
   - Username: `camiones`
   - Password: `SLN3`
   - Marcar "Save password?"
6. Hacer clic en "Save"
7. Navegar a: Servers > Transporte DB > Databases > mydb > Schemas > public > Tables
8. Aquí podrás ver y administrar todas las tablas
9. Para ver datos, hacer clic derecho en una tabla > "View/Edit Data" > "All Rows"

## Paso 8: Verificar el Servidor Flask
```bash
curl http://localhost:5000
```

Debería responder: `¡Servidor de Transporte funcionando!`

## Comandos de Verificación Rápida

### Ver estado de todos los servicios:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Ver todas las tablas creadas:
```bash
docker exec postgres_db psql -U camiones -d mydb -c "\dt"
```

### Verificar respuesta del servidor Flask:
```bash
curl http://localhost:5000
```

### Verificar que pgAdmin responde:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5050/login
```
(Debería devolver 200)

## Comandos Útiles para Desarrollo

### Ver logs del servidor Flask:
```bash
docker logs transporte_flask_app -f
```

### Ver logs de la base de datos:
```bash
docker logs postgres_db -f
```

### Ver logs de pgAdmin:
```bash
docker logs pgadmin_ui -f
```

### Reiniciar todos los servicios:
```bash
docker-compose restart
```

### Reiniciar un servicio específico:
```bash
docker-compose restart app
docker-compose restart db
docker-compose restart pgadmin
```

### Detener servicios (mantiene volúmenes y datos):
```bash
docker-compose down
```

### Detener y eliminar volúmenes (borra TODOS los datos de BD):
```bash
docker-compose down -v
```

### Reconstruir después de cambios en código:
```bash
docker-compose up -d --build
```

## Estructura de la Base de Datos

Las 10 tablas creadas son:
1. `clientes` - Información de clientes
2. `conductores` - Información de conductores
3. `rutas` - Rutas de transporte
4. `usuarios` - Usuarios del sistema
5. `vehiculos` - Flota de vehículos
6. `pedidos` - Pedidos de transporte
7. `detalles_pedido` - Detalles de cada pedido
8. `facturas` - Facturación
9. `viajes` - Viajes realizados
10. `incidencias_viaje` - Incidencias reportadas

Tabla adicional:
- `alembic_version` - Control de versiones de migraciones (sistema)

## Conexión Directa a la Base de Datos

### Desde fuera de Docker (usando psql local):
```bash
psql -h localhost -p 5433 -U camiones -d mydb
# Contraseña: SLN3
```

### Desde dentro del contenedor Docker:
```bash
docker exec -it postgres_db psql -U camiones -d mydb
```

## Notas Importantes

1. **Persistencia**: La base de datos persiste los datos en un volumen Docker llamado `transporte_pgdata`
2. **Sincronización**: Los archivos del proyecto se sincronizan en tiempo real con el contenedor (modo desarrollo) mediante el volumen `.:/app`
3. **Red Docker**: Los contenedores se comunican internamente usando el nombre del servicio (ej: `db` para la base de datos)
4. **Variables de entorno**: El archivo `.env` se usa tanto para Docker como para la aplicación Flask
5. **Credenciales**: Las credenciales por defecto son para desarrollo. CAMBIAR en producción
6. **Puertos**: 
   - Flask: 5000 (host) -> 5000 (container)
   - PostgreSQL: 5433 (host) -> 5432 (container)  
   - pgAdmin: 5050 (host) -> 80 (container)

## Solución de Problemas

### Si el servidor Flask no inicia:
```bash
docker logs transporte_flask_app
# Revisar errores de importación o configuración
```

### Si no puedes conectar pgAdmin a la BD:
- Verifica que el Host sea `db` (no localhost)
- Verifica que los contenedores estén en la misma red: `docker network inspect transporte_default`

### Si las tablas no existen:
```bash
docker exec -e FLASK_APP=run.py transporte_flask_app flask db upgrade
```
