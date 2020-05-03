from virtualassistant.models import Assistant
from virtualassistant import app, db
import os
from flask import Flask, render_template, request, redirect, flash, url_for
import string
import random
from virtualassistant import config
from PIL import Image
import urllib.request

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/assistants/create", methods=["GET"])
def assistants_create():
    return render_template("create_form.html")


@app.route("/assistants", methods=["GET", "POST"])
def assistants():
    if request.method == "GET":
        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message=None)


    elif request.method == "POST":
        if request.form:
            new_photo_name = None
            photo_path = None

            if 'photo' not in request.files:
                if new_photo_name == None:
                    new_photo_name = "{}.jpg".format(id_generator())
                if photo_path == None:
                    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], new_photo_name)

                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve("https://thispersondoesnotexist.com/image.jpg", photo_path)

                im = Image.open(photo_path)
                size = (128, 128)
                im.thumbnail(size)
                im.save(photo_path)

            file = request.files.get("photo")
            if file.filename == '':
                if new_photo_name == None:
                    new_photo_name = "{}.jpg".format(id_generator())
                if photo_path == None:
                    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], new_photo_name)

                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve("https://thispersondoesnotexist.com/image.jpg", photo_path)

                im = Image.open(photo_path)
                size = (128, 128)
                im.thumbnail(size)
                im.save(photo_path)

            if file.filename != '' and not allowed_file(file.filename):
                flash('Wrong file format. Accepted formats: png, jpg, jpeg.')
                return redirect(url_for("assistants_create"))

            if file and allowed_file(file.filename):
                photo_name, ext = os.path.splitext(file.filename)
                print("before:",new_photo_name)
                if new_photo_name == None:
                    new_photo_name = "{}{}".format(id_generator(), ext)
                    print("after:",new_photo_name)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_photo_name))
                
                if photo_path == None:
                    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], new_photo_name)

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
    if request.method == "PUT":
        assistant_to_update = Assistant.query.get(id)
        if request.form:
            assistant_to_update.name = request.form.get("name")
            assistant_to_update.surname = request.form.get("surname")
            if request.form.get("job"):
                assistant_to_update.job = request.form.get("job")

        if request.files.get("photo"):
            file = request.files.get("photo")
            if file.filename != '':
                if not allowed_file(file.filename):
                    flash('Wrong file format. Accepted formats: png, jpg, jpeg.')
                    return redirect(url_for("assistants/{}".format(id)))
                if file and allowed_file(file.filename):
                    photo_name, ext = os.path.splitext(file.filename)
                    new_photo_name = "{}{}".format(id_generator(), ext)
                    file.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], new_photo_name))
                    photo_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], new_photo_name)

                    im = Image.open(photo_path)
                    size = (128, 128)
                    im.thumbnail(size)
                    im.save(photo_path)

                    assistant_to_update.photo_name = new_photo_name
        db.session.commit()
        assistantts_all = Assistant.query.all()
        return render_template("assistants.html", assistants=assistantts_all, message="Update saved!")

@app.route("/assistants/update", methods=["GET"])
def assistants_update():
    profile_id = request.args.get('id')
    profile_to_update = Assistant.query.get(profile_id)
    return render_template("update_form.html", assistant = profile_to_update)
