from flask import Flask
from src.config import Config
from src.database.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db) 
    JWTManager(app)

    # Importar modelos y rutas
    with app.app_context():
        from src.models import actores, logistica_flota
        from src.routes.routes import main
        from src.routes.actores import bp as actores_bp
        from src.routes.logistica import bp as logistica_bp
        # from src.routes.productos import bp as productos_bp  # TODO: Crear ProductoService
        from src.routes.transacciones import bp as transacciones_bp
        from src.routes.seguimiento import bp as seguimiento_bp
        from src.routes.auth import bp as auth_bp

        if 'routes_main' not in app.blueprints:
            app.register_blueprint(main)
        if 'actores' not in app.blueprints:
            app.register_blueprint(actores_bp)
        if 'logistica' not in app.blueprints:
            app.register_blueprint(logistica_bp)
        # if 'operaciones' not in app.blueprints:
        #     app.register_blueprint(productos_bp)
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
