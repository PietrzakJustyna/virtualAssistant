from virtualassistant.models import Assistant
from virtualassistant.config import project_dir
from virtualassistant import app, db
import os
import sys
import unittest

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
        db.session.add(fake_assistant1)
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
        assistants_before = len(Assistant.query.all())
        new_assistant = Assistant(name="Bartosz",
                                  surname="Trud",
                                  job="2nd Grade Teacher",
                                  photo_path="./static/uploads/default.jpg"
                                  )
        db.session.add(new_assistant)
        db.session.commit()

        assistants_after = len(Assistant.query.all())

        self.assertEqual(assistants_after, assistants_before + 1)


if __name__ == "__main__":
    unittest.main()
