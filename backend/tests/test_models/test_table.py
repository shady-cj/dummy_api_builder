"""
Test table model
"""
import sqlalchemy
from tests import TestConfig
from models.table import Table
from models.api import Api
from models.user import User

class TestTable(TestConfig):
    """
    Full test on the Table model.
    """
    def setUp(self):
        super().setUp()
        self.user1 = User(email='user1@test.com', password='password')
        self.user2 = User(email='user2@test.com', password='password')
        self.api_1 = Api(name="test", description="description")
        self.api_2 = Api(name="test2", description="description")


    def test_create_table_for_api(self):
        """Test creating a table associated with an api"""
        with self.app.app_context():
            self.db.session.add_all([self.user1, self.user2, self.api_1, self.api_2])
            self.db.session.commit()
            # Adding the api to a specific user


            self.api_1.user_id = self.user1.id
            self.api_2.user_id = self.user2.id


            # self.db.session.commit()

            new_table = Table(name="Table1", description="test table", api_id=self.api_1.id)
            new_table_2 = Table(name="Table1", description="test table", api_id=self.api_2.id)
            self.db.session.add_all([new_table, new_table_2])
            self.db.session.commit()
            self.assertEqual(len(Table.query.all()), 2)

            self.assertEqual(new_table.api_id, self.api_1.id)
            self.assertEqual(new_table_2.api_id, self.api_2.id)

            #Check the user that owns the table and api
            self.assertEqual(new_table.api.user, self.user1)
            self.assertEqual(new_table_2.api.user, self.user2)

            self.assertEqual(new_table.entry_lists, [])
            self.assertEqual(new_table.table_parameters, [])

            #check reverse relationship

            self.assertIn(new_table, Api.query.filter_by(user_id=self.user1.id).first().tables)
            self.assertIn(new_table_2, Api.query.filter_by(user_id=self.user2.id).first().tables)


    def test_create_table_by_attaching_api_after_creation(self):
        """
        Test the creation of a table and attaching it to an api after creation
        """
        with self.app.app_context():
            self.db.session.add_all([self.user1, self.user2, self.api_1, self.api_2])
            self.db.session.commit()
            # Adding the api to a specific user


            self.api_1.user_id = self.user1.id
            self.api_2.user_id = self.user2.id


            # self.db.session.commit()

            new_table = Table(name="Table1", description="test table")
            new_table_2 = Table(name="Table1", description="test table")

            self.db.session.add_all([new_table, new_table_2])
            self.db.session.commit()

            new_table.api_id = self.api_1.id
            new_table_2.api_id = self.api_2.id

            self.assertEqual(new_table.api_id, self.api_1.id)
            self.assertEqual(new_table_2.api_id, self.api_2.id)

            #Check the user that owns the table and api
            self.assertEqual(new_table.api.user, self.user1)
            self.assertEqual(new_table_2.api.user, self.user2)

            self.assertEqual(new_table.entry_lists, [])
            self.assertEqual(new_table.table_parameters, [])

            #check reverse relationship

            self.assertIn(new_table, Api.query.filter_by(user_id=self.user1.id).first().tables)
            self.assertIn(new_table_2, Api.query.filter_by(user_id=self.user2.id).first().tables)


    def test_create_table_without_name(self):
        """
        Testing table creation without name attribute
        """
        with self.app.app_context():
            self.db.session.add_all([self.user1,self.api_1])
            self.db.session.commit()
            # Adding the api to a specific user
            self.api_1.user_id = self.user1.id
            with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
                new_table = Table(description="new table", api_id=self.api_1.id)
                self.db.session.add(new_table)
                self.db.session.commit()
            



