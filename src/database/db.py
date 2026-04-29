# src/database/db.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

class Base(object):
    def to_dict(self):
        # Convierte automáticamente cualquier modelo en un diccionario
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

db = SQLAlchemy(model_class=Base)