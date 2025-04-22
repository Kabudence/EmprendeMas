# from flask import Blueprint, request, jsonify
# from app import db
# from app.models.publicacion import Publicacion
#
#
# publicacion_bp = Blueprint('publicacion_bp', __name__)
#
#
# @publicacion_bp.route('/publicaciones/<int:id>', methods=['GET'])
# def get_publicacion(id):
#     publicacion = Publicacion.query.get(id)
#     if not publicacion:
#         return jsonify({'error': 'Publicación no encontrada'}), 404
#
#     return jsonify({
#         'id': publicacion.id,
#         'cliente_id': publicacion.cliente_id,
#         'nombre_cancion': publicacion.nombre_cancion,
#         'cancion': base64.b64encode(publicacion.cancion).decode('utf-8') if publicacion.cancion else None,
#         'fecha_publicacion': publicacion.fecha_publicacion.isoformat(),
#         'fotos': [foto.to_dict() for foto in publicacion.fotos]
#     })
