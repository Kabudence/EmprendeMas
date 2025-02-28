from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db

bp = Blueprint('ofertas', __name__, url_prefix='/ofertas')


@bp.route('/', methods=['GET'])
def get_all_ofertas():
    try:
        # Consulta para obtener todas las ofertas con campos específicos
        query = text("""
            SELECT 
                id,
                nombre,
                precio_oferta,
                precio_desc,
                precio_2x1,
                precio_paquete,
                precio_seg,
                tipo
                

            FROM ofertas
        """)
        result = db.session.execute(query).mappings()  # Usar .mappings() para obtener diccionarios

        # Procesar resultados para extraer solo el precio que no es null
        ofertas = []
        for row in result:
            precio_final = next(
                (row[key] for key in ['precio_oferta', 'precio_desc', 'precio_2x1', 'precio_paquete','precio_seg'] if row[key] is not None),
                None
            )

            ofertas.append({
                'id': row['id'],
                'nombre': row['nombre'],
                'precio_final': precio_final,
                'tipo': row['tipo']


            })

        return jsonify(ofertas)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/detalles', methods=['GET'])
def get_detalles_oferta():
    try:
        # Obtener ID de la oferta desde parámetros de la URL
        id_oferta = request.args.get('id')
        if not id_oferta:
            return jsonify({'error': 'Parámetro "id" requerido'}), 400

        # Consulta detallada con joins y filtro por ID
        query = text("""
            SELECT 
                ofertas.id,
                ofertas.tipo,
                ofertas.nombre,
                ofertas.descripcion,
                tamanios.nombre AS tamanio,
                colores.nombre AS color,
                detalles.stock,
                detalles.precio,
                detalles.capacidad
            FROM ofertas
            JOIN ofertas_detalles ON ofertas.id = ofertas_detalles.id_oferta
            JOIN detalles ON detalles.id = ofertas_detalles.id_detalle
            JOIN tamanios ON detalles.tamanio_id = tamanios.id
            JOIN colores ON detalles.color_id = colores.id
            WHERE ofertas.id = :id_oferta
        """)

        result = db.session.execute(query, {'id_oferta': id_oferta}).mappings()

        # Verificar si hay resultados
        if not result:
            return jsonify({'mensaje': 'Oferta no encontrada'}), 404

        # Extraer los datos comunes (id, nombre, descripcion, tipo)
        primera_fila = result.fetchone()
        datos_comunes = {
            'id': primera_fila['id'],
            'nombre': primera_fila['nombre'],
            'descripcion': primera_fila['descripcion'],
            'tipo': primera_fila['tipo']
        }

        # Construir el arreglo de detalles
        detalles = []
        detalles.append({
            'capacidad': primera_fila['capacidad'],
            'precio': primera_fila['precio'],
            'stock': primera_fila['stock'],
            'tamanio': primera_fila['tamanio'],
            'color': primera_fila['color']
        })

        # Agregar el resto de las filas al arreglo de detalles
        for row in result:
            detalles.append({
                'capacidad': row['capacidad'],
                'precio': row['precio'],
                'stock': row['stock'],
                'tamanio': row['tamanio'],
                'color': row['color']
            })

        # Combinar los datos comunes con el arreglo de detalles
        respuesta = {
            **datos_comunes,
            'detalles': detalles
        }

        return jsonify(respuesta)

    except Exception as e:
        return jsonify({'error': str(e)}), 500