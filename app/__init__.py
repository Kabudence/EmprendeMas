from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    # Registrar blueprints
    from app.routes.detalles import bp as detalles_bp
    from app.routes.productos import bp as productos_bp
    app.register_blueprint(detalles_bp)
    app.register_blueprint(productos_bp)

    return app
