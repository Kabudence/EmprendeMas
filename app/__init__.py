from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicializar extensiones
    db.init_app(app)

    # Configurar CORS con reglas específicas
    CORS(app, resources={
        r"/api/*": {  # Aplica CORS solo a rutas que comienzan con /api/
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],  # Permitir estos orígenes
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos permitidos
            "allow_headers": ["Content-Type", "Authorization"],  # Encabezados permitidos
        }
    })

    # Registrar blueprints
    from app.routes.detalles import bp as detalles_bp
    from app.routes.productos import bp as productos_bp
    from app.routes.servicios import servicios_bp
    from app.routes.fotos import foto_bp
    from app.routes.megustas import bp as megustas_bp
    from app.routes.comentario_foto import bp as comentario_foto_bp

    app.register_blueprint(detalles_bp, url_prefix="/api/detalles")  # Ajustar URL base del blueprint
    app.register_blueprint(productos_bp, url_prefix="/api/productos")  # Ajustar URL base del blueprint
    app.register_blueprint(servicios_bp, url_prefix="/api/servicios")  # Ajustar URL base del blueprint
    from app.routes import info_empresa,ofertas
    app.register_blueprint(info_empresa.bp, url_prefix="/api/info_empresa")  # Ajustar URL base del blueprint
    app.register_blueprint(ofertas.bp, url_prefix="/api/ofertas")  # Ajustar URL base del blueprint
    app.register_blueprint(foto_bp, url_prefix="/api/fotos")  # Ajustar URL base del blueprint
    app.register_blueprint(megustas_bp, url_prefix="/api/megustas")
    app.register_blueprint(comentario_foto_bp, url_prefix="/api/comentario_foto")

    return app
