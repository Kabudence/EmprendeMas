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
    app.register_blueprint(detalles_bp, url_prefix="/api/detalles")  # Ajustar URL base del blueprint
    app.register_blueprint(productos_bp, url_prefix="/api/productos")  # Ajustar URL base del blueprint
    app.register_blueprint(servicios_bp, url_prefix="/api/servicios")  # Ajustar URL base del blueprint

    return app
