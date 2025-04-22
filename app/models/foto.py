from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from app import db


class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(250), nullable=False)
    visitas = db.Column(db.Integer, default=0, nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Boolean, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    turl_foto = db.Column(db.Text, nullable=False)
    publicacion_id = db.Column(
        db.Integer,
        db.ForeignKey('publicacion.id', ondelete='CASCADE'),
        nullable=False
    )
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'visitas': self.visitas,
            'cliente_id': self.cliente_id,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'turl_foto': self.turl_foto
        }


class FotoResource(Resource):
    def get(self, foto_id=None):
        if foto_id:
            foto = Foto.query.get(foto_id)
            return jsonify(foto.to_dict()) if foto else (jsonify({'message': 'Not Found'}), 404)
        fotos = Foto.query.all()
        return jsonify([foto.to_dict() for foto in fotos])

    def post(self):
        data = request.json
        foto = Foto(
            description=data['description'],
            visitas=data['visitas'],
            cliente_id=data['cliente_id'],
            estado=data.get('estado', None),
            turl_foto=data['turl_foto']  # Se espera "turl_foto" en el JSON
        )
        db.session.add(foto)
        db.session.commit()
        return jsonify({'message': 'Foto created successfully', 'foto': foto.to_dict()})

    def put(self, foto_id):
        foto = Foto.query.get(foto_id)
        if not foto:
            return jsonify({'message': 'Not Found'}), 404
        data = request.json
        foto.description = data.get('description', foto.description)
        foto.visitas = data.get('visitas', foto.visitas)
        foto.cliente_id = data.get('cliente_id', foto.cliente_id)
        foto.estado = data.get('estado', foto.estado)
        foto.turl_foto = data.get('turl_foto', foto.turl_foto)
        db.session.commit()
        return jsonify({'message': 'Foto updated successfully', 'foto': foto.to_dict()})

    def delete(self, foto_id):
        foto = Foto.query.get(foto_id)
        if not foto:
            return jsonify({'message': 'Not Found'}), 404
        db.session.delete(foto)
        db.session.commit()
        return jsonify({'message': 'Foto deleted successfully'})


