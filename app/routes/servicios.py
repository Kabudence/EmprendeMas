from flask import Blueprint, jsonify, request
from app.models.servicios import Servicio
from app import db

servicios_bp = Blueprint('servicios', __name__, url_prefix='/servicios')

@servicios_bp.route('/', methods=['GET'])
def get_all_servicios():
    try:
        servicios = Servicio.query.all()
        return jsonify([servicio.to_dict() for servicio in servicios]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@servicios_bp.route('/<int:servicio_id>', methods=['GET'])
def get_servicio_by_id(servicio_id):
    try:
        servicio = Servicio.query.get(servicio_id)
        if servicio:
            return jsonify(servicio.to_dict()), 200
        return jsonify({"error": "Servicio no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
