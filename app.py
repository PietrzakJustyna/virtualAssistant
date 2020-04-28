import os

from flask import Flask
from flask import render_template
from flask_migrate import Migrate
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "virtualassistant.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Assistant(db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    surname = db.Column(db.String(64), nullable = False)

    def __repr__(self):
        return "{} {}>".format(self.name, self.surname)

@app.route("/assistants/create", methods=["GET"])
def assistants_create():
    return render_template("index.html")

@app.route("/assistants", methods=["GET", "POST"])
def assistants():
    if request.method == "GET":
        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message=None)
    else:
        if request.form:
            assistant = Assistant(name=request.form.get("name"), surname=request.form.get("surname"))
            db.session.add(assistant)
            db.session.commit()

        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message="New assistant added!")

@app.route("/assistants/<int:id>", methods=["PUT", "DELETE"])
def assistants_changes(id):
    if request.method == "DELETE":
        assistant_to_delete = Assistant.query.get(id)
        db.session.delete(assistant_to_delete)
        db.session.commit()
        return render_template("assistants.html")

  
if __name__ == "__main__":
    app.run(debug=True)

