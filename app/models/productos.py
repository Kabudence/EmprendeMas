from app import db

class Productos(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    marca = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
