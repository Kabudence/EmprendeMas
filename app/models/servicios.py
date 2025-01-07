from app import db

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    precio_oferta = db.Column(db.Float, nullable=True)
    imagen = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "precio_oferta": self.precio_oferta,
            "imagen": self.imagen,
            "telefono": self.telefono,
            "correo": self.correo,
            "categoria_id": self.categoria_id
        }
