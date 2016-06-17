from init import auth, app, api
from flask import g, jsonify, make_response
from controllers.productos import Productos
from controllers.usuarios import Usuarios
from models import Usuario



@app.route("/")
def index():
	return "HW"

@app.errorhandler(404)
def not_found(error):
	response = {
		"error": True,
		"message": "No encontrado"
	}
	return make_response(jsonify(response), 404)

@auth.verify_password
def verify_password(usuario_or_token, clave):
	user = Usuario.verify_auth_token(usuario_or_token)
	if not user:
		user = Usuario.query.filter_by(usuario=usuario_or_token).first()
		if not user or not user.login(clave):
			return False
	g.user = user
	return True

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})

api.add_resource(Productos, 
	'/api/producto', 
	'/api/producto/<int:id>')
api.add_resource(Usuarios, '/api/usuario')

if __name__ == "__main__":
	app.run(debug=True)