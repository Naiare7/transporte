from flask import Flask
# Añadimos "src." a los imports para que Python no se pierda al arrancar desde fuera
from src.config import Config
from src.database.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    # Cargar la configuración
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db) 
    JWTManager(app)

    # Importar modelos (para que Flask y Migrate sepan que existen al arrancar)
    with app.app_context():
        from src.models import actores, logistica_flota
        from src.routes.routes import main  # Importar las rutas después de los modelos 
        
        if 'routes_main' not in app.blueprints:
         app.register_blueprint(main)

    @app.route('/')
    def index():
        return "¡Servidor de Transporte con estructura perfecta funcionando!"


    return app

# app = create_app()