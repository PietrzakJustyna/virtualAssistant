from models import Assistant
from app import app, db
import os
from flask import Flask, render_template, request, redirect, flash, url_for
import string
import random
import config

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/assistants/create", methods=["GET"])
def assistants_create():
    return render_template("index.html")

@app.route("/assistants", methods=["GET", "POST"])
def assistants():
    if request.method == "GET":
        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message=None)
    elif request.method == "POST":
        if request.form:
            if 'file' not in request.files:
                photo_path = "./static/uploads/default.jpg"
        file = request.files.get("photo")
        if file.filename == '':
            photo_path = "./static/uploads/default.jpg"
        if not allowed_file(file.filename):
            flash('Wrong file format. Accepted formats: png, jpg, jpeg.')
            return redirect(url_for("assistants_create"))
        if file and allowed_file(file.filename):
            photo_name, ext = os.path.splitext(file.filename)
            new_photo_name = "{}.{}".format(id_generator(), ext)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_photo_name))
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], new_photo_name)
            im = Image.open(photo_path)
            size = (128, 128)
            im.thumbnail(size)
            im.save(photo_path)

        assistant = Assistant(name=request.form.get("name"), 
                                surname=request.form.get("surname"), 
                                job=request.form.get("job"),
                                photo_path = photo_path)

        db.session.add(assistant)
        db.session.commit()

        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message="New assistant added!")

@app.route("/assistants/<int:id>", methods=["PUT", "DELETE"])
def assistants_changes(id):
    if request.method == "DELETE":
        assistant_to_delete = Assistant.query.get(id)
        if "default" not in assistant_to_delete.photo_path:
            os.remove(assistant_to_delete.photo_path)

        db.session.delete(assistant_to_delete)
        db.session.commit()
        return render_template("assistants.html")
    if request.method(id) == "PUT":
        if request.form:
            assistant_to_update = Assistant.query.get(id)
            assistant_to_update.name = request.form.get("name")
            assistant_to_update.surname = request.form.get("surname")
            db.session.commit()

        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message="Update saved!")

@app.route("/assistants/update", methods=["GET"])
def assistants_update():
    return render_template("index.html")