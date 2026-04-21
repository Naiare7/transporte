import os
from dotenv import load_dotenv

# 1. Encontrar la ruta absoluta de la carpeta raíz (donde está run.py y .env)
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 2. Cargar el archivo .env explícitamente desde esa ruta
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # 3. Leer las variables
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')