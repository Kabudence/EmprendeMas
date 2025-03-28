
from datetime import datetime
from app import db


class Megusta(db.Model):
    Foto_id = db.Column(db.Integer, db.ForeignKey('foto.id'), primary_key=True)
    Clientes_id = db.Column(db.Integer, primary_key=True)
    fecha_like = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'Foto_id': self.Foto_id,
            'Clientes_id': self.Clientes_id,
            'fecha_like': self.fecha_like
        }




