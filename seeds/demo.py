from flask_seeder import Seeder, Faker, generator
from flask_seeder.generator import Generator
import sys
from virtualassistant.models import Assistant
from urllib.request import urlopen
import json

def get_jsonparsed_data(url):
    lines = []
    response = urlopen(url)
    data = response.read().decode("utf-8")
    json_dict = json.loads(data)

    for elem in json_dict:
        if elem.get("title") is not None:
            lines.append(elem.get("title"))

    return lines

class Job(Generator):
    """ Job generator from json list"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random job title from the list

        Returns:
            A random job title in string format
        """
        if self._lines is None:
            self._lines = get_jsonparsed_data("http://api.dataatwork.org/v1/jobs")

        result = self.rnd.choice(self._lines)

        return result


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
        "job": Job(),
        "photo_path": "./static/uploads/default.jpg"
      }
    )

    # Create 5 users
    for elem in faker.create(5):
      print("Adding assistant: %s" % elem)
      self.db.session.add(elem)