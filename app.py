import json, base64
from flask import Flask, request,jsonify, abort
from flask.views import MethodView
from flask_restful import reqparse, abort, Api, Resource
from config import app,db
from model import Location, Users
from sqlalchemy import Float, column, func, select
from sqlalchemy.orm import column_property

api = Api(app)
@app.route('/')
@app.route('/index')
def index():
	return "Welcome to location finder"

def validate_auth():
	auth = request.authorization
	if not auth:
		abort(401)
	user = Users.query.filter_by(username = auth.username).first()
	if user is None or user.password != base64.b64encode(auth.password):
		abort(401)
 
class View(MethodView):

	def get(self, name=None):
		validate_auth()
		loc = Location.query.filter_by(name=name).first()
		location = Location
		longitude = loc.lng
		latitude = loc.lat
		query = select([location.name]).where(func.earth_box(
			func.ll_to_earth(location.lat,location.lng), 3000 
				)).op('@>').func.ll_to_earth(longitude,latitude)
		result = Location.query.query
		return result
	def post(self):
		validate_auth()
		name = request.json['name']
		lat = request.json['lat']
		lng = request.json['lng']
		location = Location(name, lat, lng)
		db.session.add(location)
		db.session.commit()
		return jsonify({location.id:{
			'name' : location.name,
			'lat' : location.lat,
			'lng' : location.lng
			}})

view = View.as_view('view')
app.add_url_rule(
	'/location', view_func = view, methods=['POST']
	)
app.add_url_rule(
	'/location/<string:name>', view_func = view, methods=['GET']
	)

app.run(debug=True) 