# virtualAssistant

## About
Project was created as a recruitment task and follows requirements given. 

## Technologies used
Project was built using Flask (microframework of Python programming language). Some additional Flask libraries were used as well such as:

flask-sqlalchemy
flask-migrate
pillow
flask-seeder

## Setup
Assuming you already have Python, pip and venv prepared. 
* Install dependencies. Inside project directory run:
    `pip3 install -r requirements.txt`

* Prepare database
Run `Python3` to open Python3 CLI. Inside run:
    `from virtualassistant import db`
    `db.create_all`
    `exit()`

* Populate the database using the oreoared seeder. 
    `flask seed run`

* Start the application in development environment (debug = True).
    `python3 run.py`

## Testing
Unittests are prepared in test_virtualassistant.py. To use them to test the app run:
    `python3 test_virtualassistant.py`

## App description
Following app is a simple CRUD virtual assistant management site.
We have following functionalities:

* GET /assistants – displaying all assistants 
GET /assistants/create – displaying create form
* POST /assistants – storing new profiles
* GET /assistants/update – displaying update form
* PUT /assistants/{id} – updates assistant profile
* DELETE /assistants/{id} – deletes profile

