from flask import jsonify
from app import app, Camion

@app.route('/camiones', methods=['GET'])
def get_camiones():
    lista_camiones = Camion.query.all()
    return jsonify([c.to_dict() for c in lista_camiones]), 200

if __name__ == '__main__':
    app.run(debug=True)