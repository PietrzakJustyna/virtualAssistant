from virtualassistant.models import Assistant
from virtualassistant.config import project_dir
from virtualassistant import app, db
import os
import sys
import unittest
from werkzeug.datastructures import FileStorage

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(project_dir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        fake_assistant1 = Assistant(name="Ana",
                                    surname="Markez",
                                    job="1st Grade Teacher",
                                    photo_path="./static/uploads/default.jpg"
                                    )
        fake_assistant2 = Assistant(name="Jan",
                                    surname="Kowalski",
                                    job="Trader",
                                    photo_path="./static/uploads/default.jpg"
                                    )
        db.session.add(fake_assistant1)
        db.session.add(fake_assistant2)
        db.session.commit()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.drop_all()


###############
#### tests ####
###############

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_assistant(self):

        with app.test_client() as client:
     
            assistants_before = len(Assistant.query.all())
            data = {"name":"Bartosz",
                            "surname":"Trud",
                            "job":"2nd Grade Teacher",
            }

            photo = os.path.join("test_assets/image.jpeg")

            with open(photo, "rb") as photo:

                data['photo'] = photo
                client.post("/assistants", data=data, content_type='multipart/form-data')

            assistants_after = len(Assistant.query.all())
            new_assistant = Assistant.query.filter_by(name=data["name"], surname=data["surname"]).first()
            os.remove((new_assistant.photo_path).replace(".", "virtualassistant", 1))
            self.assertEqual(assistants_after, assistants_before + 1)


    def test_delete_assistant(self):

        with app.test_client() as client:
     
            assistants_before = len(Assistant.query.all())
            assistant_to_delete = Assistant.query.first()

            client.delete("/assistants/{}".format(assistant_to_delete.id))

            assistants_after = len(Assistant.query.all())
            self.assertEqual(assistants_after, assistants_before - 1)

if __name__ == "__main__":
    unittest.main()
