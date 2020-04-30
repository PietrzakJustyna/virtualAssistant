from flask_seeder import Seeder, Faker, generator
import sys
sys.path.append("..")
from virtualassistant.models import Assistant

# All seeders inherit from Seeder
class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    faker = Faker(
      cls=Assistant,
      init={
        "id": generator.Sequence(),
        "name": generator.Name(),
        "surname": generator.Name(),
        "job": generator.Job(),
        "photo_path": "./static/uploads/default.jpg"
      }
    )

    # Create 5 users
    for elem in faker.create(5):
      print("Adding assistant: %s" % elem)
      self.db.session.add(elem)