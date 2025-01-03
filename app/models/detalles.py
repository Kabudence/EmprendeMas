from app import db

class Detalles(db.Model):
    __tablename__ = 'detalles'
    id = db.Column(db.Integer, primary_key=True)
    color_id = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    precio = db.Column(db.Float)
    precio_anterior = db.Column(db.Float)
    descuento = db.Column(db.String(10))
    imagen = db.Column(db.String(255))
