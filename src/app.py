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

    db.init_app(app)
    Migrate(app, db) 
    JWTManager(app)

    with app.app_context():
        from src.models import actores, logistica_flota
        db.create_all()
        
        from src.routes.actores import bp as actores_bp
        from src.routes.logistica import bp as logistica_bp
        from src.routes.transacciones import bp as transacciones_bp
        from src.routes.seguimiento import bp as seguimiento_bp
        from src.routes.auth import bp as auth_bp
        from src.web.views import web_bp

        if 'actores' not in app.blueprints:
            app.register_blueprint(actores_bp, url_prefix='/api')
        if 'logistica' not in app.blueprints:
            app.register_blueprint(logistica_bp, url_prefix='/api')
        if 'transacciones' not in app.blueprints:
            app.register_blueprint(transacciones_bp, url_prefix='/api')
        if 'seguimiento' not in app.blueprints:
            app.register_blueprint(seguimiento_bp, url_prefix='/api')
        if 'auth' not in app.blueprints:
            app.register_blueprint(auth_bp, url_prefix='/api')
        if 'web' not in app.blueprints:
            app.register_blueprint(web_bp, url_prefix='/web')
       
        print("¡Rutas registradas correctamente!")

    @app.route('/')
    def index():
        return "¡Servidor de Transporte funcionando!"

    return app