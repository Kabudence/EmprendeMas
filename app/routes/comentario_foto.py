from flask import Blueprint, request, jsonify
from app import db
from app.models.comentario_foto import ComentarioFoto

bp = Blueprint('comentario_foto', __name__)

# Ruta para agregar un comentario a una foto (POST /api/comentario_foto/add)
@bp.route('/add', methods=['POST'])
def add_comentario_foto():
    data = request.get_json()
    required_fields = ['Foto_id', 'cliente_id', 'Comentarios_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Falta alguno de los campos requeridos: Foto_id, cliente_id y Comentarios_id'}), 400

    nuevo_comentario = ComentarioFoto(
        Foto_id=data['Foto_id'],
        cliente_id=data['cliente_id'],
        Comentarios_id=data['Comentarios_id']
    )
    db.session.add(nuevo_comentario)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo agregar el comentario a la foto', 'detalle': str(e)}), 500

    return jsonify(nuevo_comentario.to_dict()), 201

# Ruta para obtener todos los comentarios de una foto (GET /api/comentario_foto/<foto_id>)
@bp.route('/<int:foto_id>', methods=['GET'])
def get_comentarios_by_foto(foto_id):
    comentarios = ComentarioFoto.query.filter_by(Foto_id=foto_id).all()
    comentarios_list = [comentario.to_dict() for comentario in comentarios]
    return jsonify(comentarios_list), 200

# Ruta para eliminar un comentario de una foto (DELETE /api/comentario_foto/delete)
@bp.route('/delete', methods=['DELETE'])
def delete_comentario_foto():
    data = request.get_json()
    required_fields = ['Foto_id', 'cliente_id', 'Comentarios_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Falta alguno de los campos requeridos: Foto_id, cliente_id y Comentarios_id'}), 400

    comentario = ComentarioFoto.query.filter_by(
        Foto_id=data['Foto_id'],
        cliente_id=data['cliente_id'],
        Comentarios_id=data['Comentarios_id']
    ).first()
    if not comentario:
        return jsonify({'error': 'El comentario especificado no existe'}), 404

    db.session.delete(comentario)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo eliminar el comentario de la foto', 'detalle': str(e)}), 500

    return jsonify({'mensaje': 'Comentario de la foto eliminado exitosamente'}), 200
