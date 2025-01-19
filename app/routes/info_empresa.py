from flask import jsonify, Blueprint
from sqlalchemy import text

from app import db

bp = Blueprint('info_empresa', __name__)

@bp.route('/info', methods=['GET'])
def get_info_empresa():
    query = db.session.execute(text("SELECT * FROM info_empresa;")).mappings()
    resultados = [dict(row) for row in query]
    return jsonify(resultados), 200


# crear vista en mysql
# CREATE VIEW info_empresa AS
# SELECT
#     empresa.idEmpresa,
#     empresa.Nombre AS nombre_empresa,
#     color.Nombre_principal AS color_empresa,
# 	imagen.Filename AS logo_empresa,
#     GROUP_CONCAT(video.Url ORDER BY video.idVideo SEPARATOR ', ') AS video_urls
# FROM
#     empresa
# JOIN
#     color ON color.idEmpresa = empresa.idEmpresa
# JOIN
#     imagen ON imagen.idEmpresa = empresa.idEmpresa
# LEFT JOIN
#     video ON video.idEmpresa = empresa.idEmpresa
# WHERE
#     imagen.Tipo_imagen = 'logo'
# GROUP BY
#     empresa.idEmpresa, nombre_empresa, color_empresa, logo_empresa;