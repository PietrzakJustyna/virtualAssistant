from flask_seeder import Seeder, Faker, generator
from flask_seeder.generator import Generator
import sys
from virtualassistant.models import Assistant
import urllib.request
import json
from virtualassistant.routes import id_generator
import os
from PIL import Image

def photo_path_generator():
    new_photo_name = "{}.jpg".format(id_generator())
    photo_path = os.path.join('virtualassistant/static/uploads', new_photo_name)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve("https://thispersondoesnotexist.com/image.jpg", photo_path)

    im = Image.open(photo_path)
    size = (128, 128)
    im.thumbnail(size)
    im.save(photo_path)

    return photo_path

def get_jsonparsed_data(url):
    lines = []
    response = urllib.request.urlopen(url)
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
            self._lines = get_jsonparsed_data(
                "http://api.dataatwork.org/v1/jobs")

        result = self.rnd.choice(self._lines)

        return result

class Photo(Generator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lines = None

    def generate(self):
        """ Generate a random photo from thispersondoesntexist.com

        Returns:
            A saved photo path in string format
        """

        if self._lines is None:
            self._lines = photo_path_generator()

        result = self._lines

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
                "photo_path": Photo()
            }
        )

        # Create 10 users
        for elem in faker.create(10):
            print("Adding assistant: %s" % elem)
            self.db.session.add(elem)
