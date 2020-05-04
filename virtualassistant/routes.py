from virtualassistant.models import Assistant
from virtualassistant import app, db
import os
from flask import Flask, render_template, request, redirect, flash, url_for
import string
import random
from virtualassistant import config
from PIL import Image
import urllib.request

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, ValidationError
from wtforms.validators import DataRequired, Regexp

def alpha_val(form, field):
    if not field.data.isalpha():
        raise ValidationError("Please use only letters")

class CreateForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), alpha_val])
    surname = StringField('surname', validators=[DataRequired(), alpha_val])
    job = StringField('job', validators=[DataRequired()])
    photo = FileField()

class UpdateForm(FlaskForm):
    name = StringField('name', validators=[alpha_val])
    surname = StringField('surname', validators=[alpha_val])
    job = StringField('job')
    photo = FileField()

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/assistants/create", methods=["GET"])
def assistants_create():
    myform = CreateForm(request.form)
    return render_template("create_form.html", form = myform)


@app.route("/assistants", methods=["GET", "POST"])
def assistants():
    myform = CreateForm(request.form)
    if request.method == "GET":
        assistantts_all = Assistant.query.order_by(
            Assistant.created_on.desc()).all()
        return render_template("assistants.html", assistants=assistantts_all, message=None)
    elif request.method == "POST" and myform.validate_on_submit():
        if request.form:
            new_photo_name = None
            photo_path = None

            if "photo" not in request.files:
                if new_photo_name == None:
                    new_photo_name = "{}.jpg".format(id_generator())
                if photo_path == None:
                    photo_path = os.path.join(
                        app.config["UPLOAD_FOLDER"], new_photo_name)

                opener = urllib.request.build_opener()
                opener.addheaders = [("User-agent", "Mozilla/5.0")]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(
                    "https://thispersondoesnotexist.com/image.jpg", photo_path)

                im = Image.open(photo_path)
                size = (128, 128)
                im.thumbnail(size)
                im.save(photo_path)

            else:
                file = request.files.get("photo")

                if file.filename == "":
                    if new_photo_name == None:
                        new_photo_name = "{}.jpg".format(id_generator())
                    if photo_path == None:
                        photo_path = os.path.join(
                            app.config["UPLOAD_FOLDER"], new_photo_name)

                    opener = urllib.request.build_opener()
                    opener.addheaders = [("User-agent", "Mozilla/5.0")]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(
                        "https://thispersondoesnotexist.com/image.jpg", photo_path)

                    im = Image.open(photo_path)
                    size = (128, 128)
                    im.thumbnail(size)
                    im.save(photo_path)

                if file.filename != "" and not allowed_file(file.filename):
                    flash("Wrong file format. Accepted formats: png, jpg, jpeg.")
                    return redirect(url_for("assistants_create"))

                if file and allowed_file(file.filename):
                    photo_name, ext = os.path.splitext(file.filename)
                    if new_photo_name == None:
                        new_photo_name = "{}{}".format(id_generator(), ext)

                    file.save(os.path.join(
                        app.config["UPLOAD_FOLDER"], new_photo_name))

                    if photo_path == None:
                        photo_path = os.path.join(
                            app.config["UPLOAD_FOLDER"], new_photo_name)

                    im = Image.open(photo_path)
                    size = (128, 128)
                    im.thumbnail(size)
                    im.save(photo_path)

        assistant = Assistant(name=request.form.get("name"),
                              surname=request.form.get("surname"),
                              job=request.form.get("job"),
                              photo_name=new_photo_name)

        db.session.add(assistant)
        db.session.commit()

        assistantts_all = Assistant.query.order_by(Assistant.created_on.desc()).all()
        return render_template("assistants.html", assistants=assistantts_all, message="New assistant added!")
    else:
        flash("Insert correct data! Use only letters")
        return redirect(url_for("assistants_create"))


@app.route("/assistants/<int:id>", methods=["PUT", "DELETE"])
def assistants_changes(id):
    myform = UpdateForm(request.form)
    if request.method == "DELETE":
        assistant_to_delete = Assistant.query.get(id)
        # os.remove("virtualassistant/static/uploads/" + assistant_to_delete.photo_name)

        db.session.delete(assistant_to_delete)
        db.session.commit()
        return render_template("assistants.html")

    if request.method == "PUT" and myform.validate_on_submit():

        assistant_to_update = Assistant.query.get(id)
        if request.form:

            assistant_to_update.name = request.form.get("name")
            assistant_to_update.surname = request.form.get("surname")
            if request.form.get("job"):
                assistant_to_update.job = request.form.get("job")

        if request.files.get("photo"):
            file = request.files.get("photo")
            if file.filename != "":
                if not allowed_file(file.filename):
                    flash("Wrong file format. Accepted formats: png, jpg, jpeg.")
                    return "ERROR"
                if file and allowed_file(file.filename):
                    photo_name, ext = os.path.splitext(file.filename)
                    new_photo_name = "{}{}".format(id_generator(), ext)
                    file.save(os.path.join(
                        app.config["UPLOAD_FOLDER"], new_photo_name))
                    photo_path = os.path.join(
                        app.config["UPLOAD_FOLDER"], new_photo_name)

                    im = Image.open(photo_path)
                    size = (128, 128)
                    im.thumbnail(size)
                    im.save(photo_path)

                    assistant_to_update.photo_name = new_photo_name
        db.session.commit()
        return "OK"
    else:
        flash("Insert correct data! Use only letters")
        return "ERROR"

@app.route("/assistants/update", methods=["GET"])
def assistants_update():
    profile_id = request.args.get("id")
    profile_to_update = Assistant.query.get(profile_id)
    return render_template("update_form.html", assistant=profile_to_update)


