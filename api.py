from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postres@localhost:5432/location_finder'
db = SQLAlchemy(app)

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
