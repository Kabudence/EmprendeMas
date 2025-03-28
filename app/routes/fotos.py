from flask import Blueprint, request, jsonify
from app import db
from app.models.foto import Foto

# Definición del blueprint con prefijo /api/fotos
foto_bp = Blueprint('foto_bp', __name__)

# GET /api/fotos - Obtener todas las fotos
@foto_bp.route('', methods=['GET'])
def get_fotos():
    fotos = Foto.query.all()
    return jsonify([foto.to_dict() for foto in fotos])

# GET /api/fotos/<int:foto_id> - Obtener una foto específica por id
@foto_bp.route('/<int:foto_id>', methods=['GET'])
def get_foto(foto_id):
    foto = Foto.query.get(foto_id)
    if not foto:
        return jsonify({'message': 'Foto no encontrada'}), 404
    return jsonify(foto.to_dict())

# GET /api/fotos/paginated - Obtener fotos una por una (paginación tipo deslizador)
@foto_bp.route('/paginated', methods=['GET'])
def get_fotos_paginated():
    page = request.args.get('page', 1, type=int)  # Página actual, empieza en 1
    paginated = Foto.query.order_by(Foto.fecha_creacion.desc()).paginate(page=page, per_page=1, error_out=False)

    if not paginated.items:
        return jsonify({'message': 'No hay más fotos'}), 404

    foto = paginated.items[0]
    # Incrementar visitas de la foto
    foto.visitas += 1
    db.session.commit()

    return jsonify({
        'foto': foto.to_dict(),
        'pagina_actual': page,
        'hay_mas': paginated.has_next  # Indica si hay más fotos disponibles
    })


from datetime import datetime, timedelta  # Asegúrate de importar estos módulos

@foto_bp.route('', methods=['POST'])
def create_foto():
    data = request.get_json()
    cliente_id = data['cliente_id']

    # Calcular el inicio (lunes) y fin (domingo) de la semana actual en UTC
    hoy = datetime.utcnow()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_semana = inicio_semana + timedelta(days=6)
    fin_semana = fin_semana.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Contar las fotos subidas esta semana por el cliente
    conteo_fotos = Foto.query.filter(
        Foto.cliente_id == cliente_id,
        Foto.fecha_creacion >= inicio_semana,
        Foto.fecha_creacion <= fin_semana
    ).count()

    if conteo_fotos >= 10:
        return jsonify({
            'error': 'Límite semanal alcanzado. Máximo 10 fotos por usuario.'
        }), 400  # Código 400: Bad Request

    # Si no se excede el límite, crear la foto usando "turl_foto"
    foto = Foto(
        description=data['description'],
        visitas=data['visitas'],
        cliente_id=cliente_id,
        estado=data.get('estado', None),
        turl_foto=data['turl_foto']  # Se utiliza "turl_foto" como en el JSON de ejemplo
    )
    db.session.add(foto)
    db.session.commit()

    return jsonify({
        'message': 'Foto creada exitosamente',
        'foto': foto.to_dict()
    }), 201


# PUT /api/fotos/<int:foto_id> - Actualizar una foto existente
@foto_bp.route('/<int:foto_id>', methods=['PUT'])
def update_foto(foto_id):
    foto = Foto.query.get(foto_id)
    if not foto:
        return jsonify({'message': 'Foto no encontrada'}), 404
    data = request.get_json()
    foto.description = data.get('description', foto.description)
    foto.visitas = data.get('visitas', foto.visitas)
    foto.cliente_id = data.get('cliente_id', foto.cliente_id)
    foto.estado = data.get('estado', foto.estado)
    foto.turl_foto = data.get('turl_foto', foto.turl_foto)
    db.session.commit()
    return jsonify({'message': 'Foto actualizada exitosamente', 'foto': foto.to_dict()})

# DELETE /api/fotos/<int:foto_id> - Eliminar una foto
@foto_bp.route('/<int:foto_id>', methods=['DELETE'])
def delete_foto(foto_id):
    foto = Foto.query.get(foto_id)
    if not foto:
        return jsonify({'message': 'Foto no encontrada'}), 404
    db.session.delete(foto)
    db.session.commit()
    return jsonify({'message': 'Foto eliminada exitosamente'})


# GET /api/fotos/user/<int:cliente_id> - Obtener todas las fotos de un usuario
@foto_bp.route('/user/<int:cliente_id>', methods=['GET'])
def get_fotos_by_user(cliente_id):
    fotos = Foto.query.filter_by(cliente_id=cliente_id).all()
    if not fotos:
        return jsonify({'message': 'No se encontraron fotos para este usuario'}), 404
    return jsonify([foto.to_dict() for foto in fotos])


# GET /api/fotos/user/<int:cliente_id>/weekly - Obtener cantidad de fotos subidas esta semana por un usuario
@foto_bp.route('/user/<int:cliente_id>/weekly', methods=['GET'])
def get_weekly_fotos_by_user(cliente_id):
    # Calcular el inicio (lunes) y fin (domingo) de la semana actual en UTC
    hoy = datetime.utcnow()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_semana = inicio_semana + timedelta(days=6)
    fin_semana = fin_semana.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Contar las fotos subidas esta semana por el usuario
    count = Foto.query.filter(
        Foto.cliente_id == cliente_id,
        Foto.fecha_creacion >= inicio_semana,
        Foto.fecha_creacion <= fin_semana
    ).count()

    return jsonify({
        'cliente_id': cliente_id,
        'fotos_semanales': count
    })
