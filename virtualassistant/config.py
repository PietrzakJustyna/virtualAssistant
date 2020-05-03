import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "virtualassistant.db"))

UPLOAD_FOLDER = "virtualassistant/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

SQLALCHEMY_DATABASE_URI = database_file
secret_key = "secret"

SQLALCHEMY_TRACK_MODIFICATIONS = False
