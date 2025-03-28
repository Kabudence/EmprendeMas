from app import db

class ComentarioFoto(db.Model):
    __tablename__ = 'comentario_foto'
    Foto_id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, primary_key=True)
    Comentarios_id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {
            'Foto_id': self.Foto_id,
            'cliente_id': self.cliente_id,
            'Comentarios_id': self.Comentarios_id
        }
