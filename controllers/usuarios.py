from init import db, MyResource
from flask import abort, jsonify, request
from models import Usuario

class Usuarios(MyResource):

	def get(self):
		rows = Usuario.query.limit(10).all()

		if len(rows)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		for row in rows:
			print(row.login("1"));
			data = {
				"id": row.id,
				"usuario": row.usuario,
			}

			self.response["data"].append(data)
		
		return jsonify(self.response)

	def post(self):
		usuario = request.json.get('usuario')
		clave = request.json.get('clave')

		if usuario is None or clave is None:
			self.response["error"] = True
			self.response["message"] = "Debe ingresar el ususario y contraseña"
			return jsonify(self.response)

		if Usuario.query.filter_by(usuario=usuario).first() is not None:
			self.response["error"] = True
			self.response["message"] = "El nombre de usuario existe"
			return jsonify(self.response)

		u = Usuario(usuario=usuario, clave=clave)
		db.session.add(u)
		try:
			db.session.commit()
			self.response["data"] = {
				"id": u.id
			}
		except:
			self.response["error"] = True
			self.response["message"] = "Error al guardar informacion"

		return jsonify(self.response)