from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'aquideboponerunaclavesecreta'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/dbrewsoft2014"
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class MyResource(Resource):

	def __init__(self):
		self.response = {
			"success": True,
			"error": False,
			"message": "",
			"data": []
		}