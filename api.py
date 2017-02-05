import json
from flask_oauthlib.client import OAuth
from flask import Flask, request, jsonify, session, url_for
from flask_restful import abort, Api, Resource
from model import Location
from sqlalchemy import Float, column, func, select, text
from sqlalchemy.orm import column_property
from flask_sqlalchemy import SQLAlchemy
from config import app,db

CLIENT_ID = 'IwHI2pT2dhe8yOivHbnXFuBfg2Z6kxXJLJddNx9Z'
CLIENT_SECRET = 'q7rEbHyCFwIqWEQPNRoJy0nSniJyFZyWD2NQ2ewkz9lgJfRW9m'

oauth = OAuth(app)

remote = oauth.remote_app(
    'remote',
    consumer_key = CLIENT_ID,
    consumer_secret = CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='http://127.0.0.1:5000/api/',
    request_token_url=None,
    access_token_url='http://127.0.0.1:5000/oauth/token',
    authorize_url='http://127.0.0.1:5000/oauth/authorize'
)

@app.route('/')
@app.route('/index')
def index():
	if 'remote oauth' in session:
		resp = remote.get('user_name')
		return jsonify(resp.data)
	next_url = request.args.get('next')
	return remote.authorize(
			callback=url_for('authorized', next=next_url, _external=True)
		)

@app.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['remote_oauth'] = (resp['access_token'], '')
    return jsonify(oauth_token=resp['access_token'])
 

@app.route('/location/<string:name>', methods=['GET'])
def get(self, name=None):
	loc = Location.query.filter_by(name=name).first()
	longitude = loc.lng
	latitude = loc.lat

	query = db.session.query(Location).from_statement(
		text("SELECT location.lat, location.lng FROM location WHERE earth_box(ll_to_earth(location.lat, location.lng),1000)@>ll_to_earth("+latitude+','+longitude+")")
		)

	for locatn in query:
		return locatn

@app.route('/location', methods=['POST'])
def post():
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

@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')

app.run(host='localhost', port=8000 ,debug=True) 