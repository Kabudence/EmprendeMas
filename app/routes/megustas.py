from flask import  request, jsonify, Blueprint
from datetime import datetime
from app import db
from app.models.megusta import Megusta

bp = Blueprint('me_gusta_bp', __name__)

# Ruta para generar un like (POST /like)
@bp.route('/like', methods=['POST'])
def like():
    data = request.get_json()
    if not data or 'Foto_id' not in data or 'Clientes_id' not in data:
        return jsonify({'error': 'Se requiere Foto_id y Clientes_id'}), 400

    # Crear un nuevo like con la fecha actual
    nuevo_like = Megusta(
        Foto_id=data['Foto_id'],
        Clientes_id=data['Clientes_id'],
        fecha_like=datetime.utcnow()
    )
    db.session.add(nuevo_like)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo registrar el like', 'detalle': str(e)}), 500

    return jsonify(nuevo_like.to_dict()), 201


# Ruta para obtener el número de likes de una foto (GET /getNumberOfLikesByfotoId/<foto_id>)
@bp.route('/getNumberOfLikesByfotoId/<int:foto_id>', methods=['GET'])
def get_number_of_likes_by_foto_id(foto_id):
    # Realiza el conteo de likes de la foto indicada
    numero_likes = Megusta.query.filter_by(Foto_id=foto_id).count()
    return jsonify({'Foto_id': foto_id, 'numero_likes': numero_likes}), 200


# Ruta para eliminar un like (DELETE /dislike)
@bp.route('/dislike', methods=['DELETE'])
def dislike():
    data = request.get_json()
    if not data or 'Foto_id' not in data or 'Clientes_id' not in data:
        return jsonify({'error': 'Se requiere Foto_id y Clientes_id para eliminar el like'}), 400

    like = Megusta.query.filter_by(Foto_id=data['Foto_id'], Clientes_id=data['Clientes_id']).first()
    if not like:
        return jsonify({'error': 'El like especificado no existe'}), 404

    db.session.delete(like)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo eliminar el like', 'detalle': str(e)}), 500

    return jsonify({'mensaje': 'Like eliminado exitosamente'}), 200


# Ruta para verificar si existe un like dado por un cliente en una foto (GET /existeLike/<int:foto_id>/<int:cliente_id>)
@bp.route('/existeLike/<int:foto_id>/<int:cliente_id>', methods=['GET'])
def existe_like(foto_id, cliente_id):
    like = Megusta.query.filter_by(Foto_id=foto_id, Clientes_id=cliente_id).first()
    return jsonify({'existe': like is not None}), 200
