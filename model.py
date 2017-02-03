from api import app,manager,db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(128))
	lat = db.Column(db.String(128))
	lng = db.Column(db.String(128))

if __name__ == '__main__':
	manager.run()