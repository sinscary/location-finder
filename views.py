import json, base64
from flask import Flask, request,jsonify, abort
from flask.views import MethodView
from flask_restful import reqparse, abort, Api, Resource
from api import app,db
from model import Location, Users

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
		location = Location.query.filter_by(name=name).first()
		res = {
			'lat':location.lat,
			'lng':location.lng
		}
		return jsonify(res) #db.func.earth_box(db.func.ll_to_earth(location.lat, location.lng),30)
		

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