from flask import Blueprint, jsonify
from app.models.detalles import Detalles
from app import db  # Importar la sesión de la base de datos
from sqlalchemy import text

bp = Blueprint('detalles', __name__, url_prefix='/detalles')

@bp.route('/imagenes', methods=['GET'])
def obtener_imagenes():
    # Ejemplo de endpoint
    imagenes = [detalle.imagen for detalle in Detalles.query.all()]
    return jsonify(imagenes), 200



@bp.route('/productos', methods=['GET'])
def obtener_detalles_productos():
    # Ejecutar el query SQL directamente, usando text para consultas explícitas
    query = text("""
        SELECT 
            d.id, 
            d.producto_id, 
            d.precio, 
            d.precio_anterior, 
            d.descuento, 
            p.nombre AS producto_nombre, 
            d.imagen, 
                
        FROM 
            detalles d
        JOIN 
            productos p ON d.producto_id = p.id
    """)
    result = db.session.execute(query)
    # Convertir los resultados en una lista de diccionarios
    detalles = [
        {
            "id": row.id,
            "producto_id": row.producto_id,
            "precio": row.precio,
            "precio_anterior": row.precio_anterior,
            "descuento": row.descuento,
            "nombre": row.producto_nombre,
            "imagen": row.imagen,
            "marca": row.marca
        }
        for row in result
    ]
    return jsonify(detalles), 200