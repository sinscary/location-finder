from api import app,db

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

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()