"""
Testing Constraints model
"""

from tests import TestConfig
from models.table import Table
from models.api import Api
from models.user import User
from models.tableparameter import TableParameter
from models.constraints import Constraint
import sqlalchemy


class TestConstraints(TestConfig):
    """
      Full test on the Constraints model
    """
    def setUp(self):
        super().setUp()
        


    def cls_setup(self):
        """
        create a setup context for testing constraints methods since they'd depend on the user, api and table
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
        self.Tb_id = TableParameter(name="_id", table_id=self.table1.id, data_type="integer")
        self.Tb_name = TableParameter(name="name", table_id=self.table1.id) # Creates a table parameter of name, by default it'll would have a data type of string    
        self.Tb_age = TableParameter(name="age", data_type="integer", table_id=self.table1.id)
        self.Tb_created = TableParameter(name="created", data_type="date", table_id=self.table1.id)
        self.Tb_isStaff = TableParameter(name="isStaff", data_type="boolean", table_id=self.table1.id)
        self.Tb_email = TableParameter(name="email", dataType_length=20, table_id=self.table1.id)
        self.db.session.add_all([self.Tb_id,self.Tb_age, self.Tb_email, self.Tb_name, self.Tb_created, self.Tb_isStaff ])
        self.db.session.commit()


    def test_create_valid_constraints_for_tableparameters(self):
        """
        Test various valid table constraints 
        """
        with self.app.app_context():
            self.cls_setup()
            self.pk = Constraint(name="primary_key")
            self.fk = Constraint(name="foreign_key")
            self.nullable = Constraint(name="nullable")
            self.unique = Constraint(name="unique")

            self.db.session.add_all([self.pk, self.fk, self.unique, self.nullable])
            self.db.session.commit()
            # Add table parameters using reverse relationship
            self.pk.table_parameters.append(self.Tb_id)
            self.fk.table_parameters.append(self.Tb_email)
            self.unique.table_parameters.append(self.Tb_id)
            self.unique.table_parameters.append(self.Tb_email)
            self.nullable.table_parameters.append(self.Tb_age)
           

            self.assertIn(self.pk, self.Tb_id.constraints)
            self.assertIn(self.fk, self.Tb_email.constraints)
            self.assertIn(self.unique, self.Tb_email.constraints)
            self.assertIn(self.nullable, self.Tb_age.constraints)
            self.assertIn(self.unique, self.Tb_id.constraints)

    def test_create_invalid_constraints(self):
        """
        Test invalid constraints
        """
        with self.app.app_context():
            self.cls_setup()
            with self.assertRaises(LookupError):
                self.pk = Constraint(name="pk")
                self.fk = Constraint(name="foreign key")
                self.pk.table_parameters.append(self.Tb_id)
                self.fk.table_parameters.append(self.Tb_email)
                self.db.session.add_all([self.pk, self.fk])
                self.db.session.commit()
                self.assertIn(self.pk, self.Tb_id.constraints)
                self.assertIn(self.fk, self.Tb_email.constraints)


    def test_create_constraints_with_multiple_fields_of_same_name(self):
        """
        Test create constraints fields with more than one field with same name
        """
        with self.app.app_context():
            with self.assertRaises(sqlalchemy.exc.IntegrityError) as e:
                pk = Constraint(name="primary_key")
                pk2 = Constraint(name="primary_key")
                self.db.session.add_all([pk, pk2])
                self.db.session.commit()