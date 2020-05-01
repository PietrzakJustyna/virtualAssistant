import os
import sys
import unittest

TEST_DB = 'test.db'

from virtualassistant import app, db
from virtualassistant.config import project_dir
from virtualassistant.models import Assistant
 
 
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

        fake_assistant1 = Assistant(name= "Ana",
                                    surname= "Markez",
                                    job= "1st Grade Teacher",
                                    photo_path= "./static/uploads/default.jpg"
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
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_assistant(self):
        assistantts_all = len(Assistant.query.all())

        self.assertEqual(assistantts_all, 1)
 
 
if __name__ == "__main__":
    unittest.main()