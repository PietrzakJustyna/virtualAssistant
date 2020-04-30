from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
from PIL import Image

import config

app = Flask(__name__)

from routes import *
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.secret_key = config.secret_key
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
migrate = Migrate(app, db)
seeder = FlaskSeeder()
seeder.init_app(app, db)


if __name__ == "__main__":
    app.run(debug=True)

