import json, base64
from flask_oauthlib.provider import OAuth2Provider
from flask import Flask, request, jsonify, abort
from flask.views import MethodView
from flask_restful import abort, Api, Resource
from model import Location, Users
from sqlalchemy import Float, column, func, select, text
from sqlalchemy.orm import column_property
from flask_sqlalchemy import SQLAlchemy
from config import app,db
oauth = OAuth2Provider(app)
api = Api(app)
@app.route('/')
@app.route('/index')
def index():
	return "Welcome to location finder"
 
@oauth.usergetter
def get_user(username, password, *args, **kwargs):
	user = Users.query.filter_by(username = username).first()
	if user.check_password(password):
		return user
	return None

@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
	if request.method == 'GET':
		client_id = kwargs.get('client_id')
		client = Client.query.filter_by(client_id=client_id).first()
		kwargs['client'] = client
		redirect('/location', **kwargs)

	confirm = request.form.get('confirm', 'no')
	return confirm == 'yes'
class View(MethodView):

	def get(self, name=None):
		loc = Location.query.filter_by(name=name).first()
		longitude = loc.lng
		latitude = loc.lat

		query = db.session.query(Location).from_statement(
			text("SELECT location.lat, location.lng FROM location WHERE earth_box(ll_to_earth(location.lat, location.lng),1000)@>ll_to_earth("+latitude+','+longitude+")")
			)

		for locatn in query:
			return locatn
	def post(self):
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