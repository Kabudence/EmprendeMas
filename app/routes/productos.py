from flask import Blueprint, jsonify
from app.models.productos import Productos
from app import db

bp = Blueprint('productos', __name__, url_prefix='/productos')

@bp.route('/marcas', methods=['GET'])
def obtener_marcas():
    marcas = db.session.query(Productos.marca).distinct().all()
    marcas_unicas = [marca[0] for marca in marcas]
    return jsonify(marcas_unicas), 200
