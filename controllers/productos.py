from init import auth, MyResource
from flask import jsonify
from models import Producto
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class Productos(MyResource):

	@auth.login_required
	def get(self, id=0):
		if id>0:
			rows = Producto.query.filter_by(id=id).all()
		else:
			rows = Producto.query.limit(10).all()

		if len(rows)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		for row in rows:
			data = {
				"id": row.id,
				"nombre": row.nombre,
			}

			self.response["data"].append(data)
		
		return jsonify(self.response)