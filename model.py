from config import app,db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128))
	lat = db.Column(db.String(128))
	lng = db.Column(db.String(128))

	def __init__(self, name, lat, lng):
		self.name = name
		self.lat = lat
		self.lng = lng

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(128))
	password = db.Column(db.String(128))

	def __init__(self, username, password):
		self.username = username
		self.password = password

class Client(db.Model):
	client_id = db.Column(db.String(40), primary_key=True)
	client_secret = db.Column(db.String(55), unique=True, index=True,
					nullable=False)
	_redirect_uris = db.Column(db.Text)
	_default_scopes = db.Column(db.Text)

class Grant(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False)
	client = db.relationship('Client')
	code = db.Column(db.String(255), index=True, nullable=False)
	redirect_uri = db.Column(db.String(255))
	expires = db.Column(db.DateTime)
	_scopes = db.Column(db.Text)

class Token(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False)
	client = db.relationship('Client')
	token_type = db.Column(db.String(40))
	access_token = db.Column(db.String(255), unique=True)
	refresh_token = db.Column(db.String(255), unique=True)
	expires = db.Column(db.DateTime)
	_scopes = db.Column(db.Text)

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()