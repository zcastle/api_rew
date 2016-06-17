from init import db, app
from util import md5
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class Producto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(60))

	def __repr__(self):
		return "<Producto %r>" % self.nombre

class Usuario(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(100))
	apellido = db.Column(db.String(100))
	usuario = db.Column(db.String(100), index=True)
	clave = db.Column(db.String(32))

	def generate_auth_token(self, expiration = 600):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = Usuario.query.get(data['id'])
		return user

	def __repr__(self):
		return "<Usuario %r>" % self.usuario

	def login(self, clave):
		return self.clave == md5(clave)