from datetime import datetime

from app import db

# app/models/publicacion.py   (debería verse algo así)
class Publicacion(db.Model):
    __tablename__ = 'publicacion'        #  ←  ❌ si dice publicidad, cámbialo
    id            = db.Column(db.Integer, primary_key=True)
    cliente_id    = db.Column(db.Integer)
    nombre_cancion= db.Column(db.String(255))
    cancion       = db.Column(db.LargeBinary)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fotos         = db.relationship('Foto', backref='publicacion', lazy=True)
