from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from sqlalchemy import text
import pytz
from app import db

# Configuramos el timezone para Perú
peru_tz = pytz.timezone('America/Lima')

bp = Blueprint('publicidad', __name__, url_prefix='/publicidad')


@bp.route('/publicidad', methods=['POST'])
def insert_publicidad():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    url_redes = data.get('red')
    horas = data.get('horas')
    imagen = data.get('imagen')

    if not url_redes or not horas or not imagen:
        return jsonify({'error': 'Faltan campos requeridos (red, horas, imagen)'}), 400

    # Si 'red' es una lista, los concatenamos separados por coma
    if isinstance(url_redes, list):
        url_redes_str = ','.join(url_redes)
    else:
        url_redes_str = url_redes

    # Fecha y hora actuales en el timezone de Perú
    now = datetime.now(peru_tz)

    try:
        # Verificar si existe al menos un registro previo
        query = text("SELECT fecha_fin FROM publicidad ORDER BY id DESC LIMIT 1")
        # Usamos .mappings() para obtener el resultado como diccionario
        last = db.session.execute(query).mappings().fetchone()

        if last:
            last_fecha_fin = last['fecha_fin']
            # Si el valor obtenido es naive, le asignamos el timezone de Perú
            if last_fecha_fin.tzinfo is None:
                last_fecha_fin = peru_tz.localize(last_fecha_fin)
            # Si la fecha actual es menor que la fecha_fin del último registro, usamos ese valor como inicio
            if now < last_fecha_fin:
                fecha_inicio = last_fecha_fin
            else:
                fecha_inicio = now
        else:
            fecha_inicio = now

        # Sumamos las horas para obtener la fecha_fin de la nueva entrada
        fecha_fin = fecha_inicio + timedelta(hours=int(horas))

        # Insertamos el registro en la tabla 'publicidad'
        insert_sql = text("""
            INSERT INTO publicidad (url_redes, url_imagen, fecha_inicio, fecha_fin)
            VALUES (:url_redes, :imagen, :fecha_inicio, :fecha_fin)
        """)
        db.session.execute(insert_sql, {
            'url_redes': url_redes_str,
            'imagen': imagen,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_fin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
        })
        db.session.commit()

        return jsonify({
            # Puedes devolver las redes como un arreglo usando split()
            'url_redes': [red.strip() for red in url_redes_str.split(',')],
            'url_imagen': imagen,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_fin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500




@bp.route('/publicidad/current', methods=['GET'])
def get_current_publicidad():
    now = datetime.now(peru_tz).strftime('%Y-%m-%d %H:%M:%S')
    try:
        query = text("""
            SELECT * FROM publicidad
            WHERE fecha_inicio <= :now AND fecha_fin >= :now
            ORDER BY fecha_inicio ASC
            LIMIT 1
        """)
        result = db.session.execute(query, {'now': now}).mappings().fetchone()
        if result:
            result_dict = dict(result)
            # Convertir 'url_redes' a lista, separando por comas, si existe
            if result_dict.get('url_redes'):
                result_dict['url_redes'] = [red.strip() for red in result_dict['url_redes'].split(',')]
            return jsonify(result_dict), 200
        else:
            return jsonify({'message': 'No se encontró publicidad activa'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@bp.route('/publicidad/images/<int:num_images>', methods=['GET'])
def get_images(num_images):
    now = datetime.now(peru_tz).strftime('%Y-%m-%d %H:%M:%S')
    try:
        query = text("""
            SELECT * FROM publicidad
            WHERE fecha_fin >= :now
            ORDER BY fecha_inicio ASC
            LIMIT :num_images
        """)
        result = db.session.execute(query, {'now': now, 'num_images': num_images}).mappings().fetchall()
        records = [dict(row) for row in result]

        for rec in records:
            if rec.get('url_redes'):
                rec['url_redes'] = [red.strip() for red in rec['url_redes'].split(',')]

        return jsonify(records), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
