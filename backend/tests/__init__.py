from api.v1 import create_app
from models import db
from unittest import TestCase


class TestConfig(TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.db = db
        
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()