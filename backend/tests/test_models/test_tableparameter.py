"""
Testing tableparameter model
"""

from tests import TestConfig
from models.table import Table
from models.api import Api
from models.user import User
from models.tableparameter import TableParameter
import sqlalchemy

# class TableParameterContext()
class TestTableParameter(TestConfig):
    """
      Full test on the Table Parameter model
    """
    def setUp(self):
        super().setUp()
        


    def tb_setup(self):
        """
        To create a setup context for testing tableparameter methods since they'd depend on the user, api and table
        """
        self.user1 = User(email='user1@test.com', password='password')
        self.user2 = User(email='user2@test.com', password='password')
        self.api1 = Api(name="test", description="description")
        self.api2 = Api(name="test2", description="description")

        self.db.session.add_all([self.user1, self.user2, self.api1, self.api2])
        self.db.session.commit()
        # Adding the api to a specific user
        self.api1.user_id = self.user1.id
        self.api2.user_id = self.user2.id

        self.table1 = Table(name="Table1", description="test table", api_id=self.api1.id)
        self.table2 = Table(name="Table2", description="test table", api_id=self.api2.id)
        self.db.session.add_all([self.table1, self.table2])
        self.db.session.commit()

    
    def test_create_tableparameter_for_tables(self):
        """
        Test creation of tableparameters for a table

        """

        with self.app.app_context():
            self.tb_setup()
            new_Tb_name = TableParameter(name="name", table_id=self.table1.id) # Creates a table parameter of name, by default it'll would have a data type of string    
            new_Tb_age = TableParameter(name="age", data_type="integer", table_id=self.table1.id)
            new_Tb_created = TableParameter(name="created", data_type="date", table_id=self.table1.id)
            new_Tb_isStaff = TableParameter(name="isStaff", data_type="boolean", table_id=self.table1.id)
            new_Tb_email = TableParameter(name="email", dataType_length=20, table_id=self.table1.id)

            self.db.session.add_all([new_Tb_age, new_Tb_email, new_Tb_name, new_Tb_created, new_Tb_isStaff ])
            self.db.session.commit()

            self.assertEqual(new_Tb_name.data_type.value, "String")
            self.assertEqual(new_Tb_age.data_type.value, "Integer")
            self.assertEqual(new_Tb_created.data_type.value,"date")
            self.assertEqual(new_Tb_isStaff.data_type.value, "Boolean")
            self.assertEqual(new_Tb_email.dataType_length, 20)
            self.assertEqual(len(self.table1.table_parameters), 5)
            # self.assertL(, self.table1.table_parameters)
            for tbp in [new_Tb_age, new_Tb_created, new_Tb_email, new_Tb_isStaff, new_Tb_name]:
                self.assertIn(tbp, self.table1.table_parameters)

    def test_create_tb_with_no_name(self):
        """
        Test creation of table parameter with no name expect an error
        """
        with self.app.app_context():
            self.tb_setup()
            with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
                tb_name = TableParameter(table_id=self.table1.id)
                self.db.session.add(tb_name)
                self.db.session.commit()

    def test_create_tb_with_pk(self):
        """
        Test creation of table parameter with no name expect an error
        """
        with self.app.app_context():
            self.tb_setup()
            tb_name = TableParameter(name="name", table_id=self.table2.id)
            tb_id = TableParameter(name="id", table_id=self.table2.id, primary_key=True)

            self.db.session.add_all([tb_name, tb_id])
            self.db.session.commit()

            self.assertFalse(tb_name.primary_key)
            self.assertTrue(tb_id.primary_key)

