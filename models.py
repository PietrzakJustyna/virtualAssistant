from flask_sqlalchemy import SQLAlchemy
from app import db


class Assistant(db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    surname = db.Column(db.String(64), nullable = False)
    job = db.Column(db.String(64), nullable = False)
    photo_path = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return "{} {}, {}>".format(self.name, self.surname, self.job)