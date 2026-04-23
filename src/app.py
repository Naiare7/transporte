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

    with app.app_context():
        from src.models import actores, logistica_flota, operaciones
        from src.routes.routes import main
        
        if 'routes_main' not in app.blueprints:
            app.register_blueprint(main, url_prefix='/api')

    @app.route('/')
    def index():
        return "¡Servidor de Transporte funcionando!"

    return app
