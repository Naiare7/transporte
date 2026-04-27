from flask import Flask
from src.config import Config
from src.database.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    # Inicialización de extensiones
    db.init_app(app)
    Migrate(app, db) 
    JWTManager(app)

    # Importar modelos y rutas
    with app.app_context():
        # Importación de modelos (para que Flask-Migrate los vea)
        from src.models import actores, logistica_flota, operaciones

        # Importación de Blueprints (Rutas)
        from src.routes.routes import main
        from src.routes.actores import bp as actores_bp
        from src.routes.logistica import bp as logistica_bp
        from src.routes.transacciones import bp as transacciones_bp
        from src.routes.seguimiento import bp as seguimiento_bp
        from src.routes.auth import bp as auth_bp

        # Registro de Blueprints
        if 'routes_main' not in app.blueprints:
            app.register_blueprint(main, url_prefix='/api')
            
        if 'actores' not in app.blueprints:
            app.register_blueprint(actores_bp)
            
        if 'logistica' not in app.blueprints:
            app.register_blueprint(logistica_bp)
            
        if 'transacciones' not in app.blueprints:
            app.register_blueprint(transacciones_bp)
            
        if 'seguimiento' not in app.blueprints:
            app.register_blueprint(seguimiento_bp)
            
        if 'auth' not in app.blueprints:
            app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return "¡Servidor de Transporte funcionando!"

    return app