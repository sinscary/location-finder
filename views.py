import json
from flask import Flask, request,jsonify
from flask.views import MethodView
from flask_restful import reqparse, abort, Api, Resource
from api import app,db
from model import Location

#parser = reqparse.RequestParser()

@app.route('/')
@app.route('/index')
def index():
	return "Welcome to location finder"


 
class View(MethodView):

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
	'/location', view_func = view, methods=['GET', 'POST']
	)

app.run(debug=True) 