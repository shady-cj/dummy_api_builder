from api.v1.app import app
from run import db

from unittest import TestCase


class TestConfig(TestCase):
    def setUp(self):
        self.app = app
        self.db = db
        self.client = self.app.test_client()
        
        # self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
