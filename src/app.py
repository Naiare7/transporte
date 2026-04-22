from flask import Flask
from src.config import Config
from src.database.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Importar modelos
from src.models import actores, logistica_flota, operaciones

# =========================================================
# ¡EL PUENTE! (Asegúrate de que estas dos líneas estén aquí)
# =========================================================
from src.routes.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# Ruta de prueba inicial
@app.route('/')
def index():
    return "¡Servidor de Transporte funcionando!"