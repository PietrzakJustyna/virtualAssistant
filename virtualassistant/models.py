from flask_sqlalchemy import SQLAlchemy
from virtualassistant import db
import datetime


class Assistant(db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    job = db.Column(db.String(64), nullable=False)
    photo_path = db.Column(db.String(128), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return "{} {}, {}>".format(self.name, self.surname, self.job)
