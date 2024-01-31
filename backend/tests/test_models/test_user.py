"""
Testing the user model
"""
from tests import TestConfig
from models.user import User

import sqlalchemy

class TestUser(TestConfig):
    """
    Full test on the user model 
    """

            
    
    def test_default_user_creation(self):
        
        """
        test user creation without all the parameter
        No validation
        """


        user = User(email="test@test.com", password="password")
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.password, "password")
        self.assertIsNone(user.id)
        self.assertIsNone(user.public_id)
        self.assertIsNone(user.last_public_id_created)
        self.assertIsInstance(user.user_apis, list)

    def test_user_creation_with_db(self):
        """
        test user creation with test db
        """
        with self.app.app_context():
            user = User(email="test@test.com", password="password")
            self.db.session.add(user)
            self.db.session.commit()

            self.assertEqual(len(User.query.all()), 1)
            created_user = User.query.filter_by(email="test@test.com").first()
            self.assertIsNotNone(created_user)
            self.assertIsInstance(created_user, User)
            self.assertEqual(created_user.email, "test@test.com")
            self.assertEqual(created_user.password, "password")
            self.assertEqual(created_user.id, 1)
            
        
    
    def test_user_creation_without_email(self):
        """
        test user creation without email
        expected to raise a database table integrity error
        """

        with self.app.app_context():
           
            with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
                user = User(password="password")
                self.db.session.add(user)
                self.db.session.commit()


    def test_user_creation_without_password(self):
        """
        test user creation without a password
        expected to raise a database table integrity error 
        """
        with self.app.app_context():
           
            with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
                user = User(email="test@test.com")
                self.db.session.add(user)
                self.db.session.commit()


    def test_user_creation_with_wrong_datatype(self):
        """
        test user creation with the wrong data types
        """

        # with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
        with self.app.app_context():
            user = User(email=123, password=123)
            self.db.session.add(user)
            self.db.session.commit()

            self.assertEqual(user.id, 1)
            self.assertIsInstance(user.email, str)
            self.assertIsInstance(user.password, str)