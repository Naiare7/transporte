from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
app = Flask(__name__)

# Configuración de la DB (Asegúrate de que la contraseña coincida con la que pusiste antes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://camiones:SLN3@localhost:5432/transporte_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secreto-cambiame' # Para los tokens

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Aquí definimos cómo se ven los camiones en la base de datos.
class Camion(db.Model):
    __tablename__ = 'camiones'
    
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(20), unique=True, nullable=False)
    capacidad_toneladas = db.Column(db.Float, nullable=False)
    tipo_grano = db.Column(db.String(50)) # Trigo, Maíz, etc.
    disponible = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "patente": self.patente,
            "capacidad": self.capacidad_toneladas,
            "tipo_grano": self.tipo_grano,
            "disponible": self.disponible
        }
from routes import *
if __name__ == '__main__': app.run(debug=True)
