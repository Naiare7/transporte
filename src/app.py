from flask import Flask
# Añadimos "src." a los imports para que Python no se pierda al arrancar desde fuera
from src.config import Config
from src.database.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar la configuración
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Importar modelos (para que Flask y Migrate sepan que existen al arrancar)
from src.models import actores, vehiculos

@app.route('/')
def index():
    return "¡Servidor de Transporte con estructura perfecta funcionando!"
