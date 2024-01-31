"""
Tests the api model
"""

from tests import TestConfig
from models.api import Api
from models.user import User
import sqlalchemy


class TestApi(TestConfig):
    """
    Full test on the Api model
    """
    def setUp(self):
        super().setUp()
        self.user1 = User(email='user1@test.com', password='password')
        self.user2 = User(email='user2@test.com', password='password')
        # with self.app.app_context():
            
            

    def test_apis_creation(self):
        """
        Creating api normally
        """

        with self.app.app_context():
            self.db.session.add_all([self.user1, self.user2])
           
            self.db.session.commit()
            api_1 = Api(name="test_api", description="test api", user_id=self.user1.id)
            api_2 = Api(name="test_api_2",description="test api", user_id=self.user1.id)

            self.db.session.add_all([api_1,api_2])
            self.assertIsNone(api_1.id)
            self.assertIsNone(api_2.id)

            self.db.session.commit()
            self.assertEqual(len(Api.query.all()), 2)
            self.assertIn(api_1.id, [1, 2])
            self.assertIn(api_2.id, [1,2])

            self.assertEqual(api_1.user_id, self.user1.id)
            self.assertEqual(api_2.user_id, self.user1.id)
            self.assertEqual(api_1.user, self.user1)
            self.assertEqual(api_2.user, self.user1)
            self.assertTrue(len(self.user1.user_apis) == 2)


    def test_api_creation_without_name(self):
        """
        Creating an api without a name attribute
        """

        with self.app.app_context():

            with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
                api = Api(description="test description")
                self.db.session.add(api)

                self.db.session.commit()
    
    def test_attaching_user_after_api_creation(self):
        """
        Creating an api and then attaching a user after it's been created

        """
        with self.app.app_context():
            self.db.session.add_all([self.user1, self.user2])
           
            self.db.session.commit()
            api_1 = Api(name="test_api", description="test api")
            api_2 = Api(name="test_api_2",description="test api")
            self.db.session.add_all([api_1,api_2])

            api1 = Api.query.filter_by(name='test_api').first()
            api2 = Api.query.filter_by(name='test_api_2').first()
            api1.user_id = self.user1.id
            api2.user_id = self.user2.id
            self.assertEqual(api1.user_id, self.user1.id)
            self.assertEqual(api2.user_id, self.user2.id)
            self.assertEqual(api1.user, self.user1)
            self.assertEqual(api2.user, self.user2)
            self.assertTrue(len(self.user1.user_apis) == 1)
            self.assertTrue(len(self.user2.user_apis) == 1)

