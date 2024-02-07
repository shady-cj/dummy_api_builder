"""
Testing tableparameter model
"""

from tests import TestConfig
from models.table import Table
from models.api import Api
from models.user import User
from models.tableparameter import TableParameter
from models.constraints import Constraint
from models.entry import Entry
from models.entrylist import EntryList
import sqlalchemy

# class TableParameterContext()
class TestTableParameter(TestConfig):
    """
      Full test on the Table Parameter model
    """
    def setUp(self):
        super().setUp()

    def cls_setup(self):
        """
        create a setup context for testing entry methods since they'd depend on the user, api and table
        """
        self.user1 = User(email='user1@test.com', password='password')
        self.api1 = Api(name="test", description="description")

        self.db.session.add_all([self.user1, self.api1])
        self.db.session.commit()
        # Adding the api to a specific user
        self.api1.user_id = self.user1.id
        self.table1 = Table(name="Table1", description="test table", api_id=self.api1.id)
        self.db.session.add(self.table1)
        self.db.session.commit()
        self.Tb_id = TableParameter(name="_id", table_id=self.table1.id, data_type="integer")
        self.Tb_name = TableParameter(name="name", table_id=self.table1.id) # Creates a table parameter of name, by default it'll would have a data type of string    
        self.Tb_age = TableParameter(name="age", data_type="integer", table_id=self.table1.id)
        self.Tb_created = TableParameter(name="created", data_type="date", table_id=self.table1.id)
        self.Tb_isStaff = TableParameter(name="isStaff", data_type="boolean", table_id=self.table1.id)
        self.Tb_email = TableParameter(name="email", dataType_length=20, table_id=self.table1.id)
        self.db.session.add_all([self.Tb_id,self.Tb_age, self.Tb_email, self.Tb_name, self.Tb_created, self.Tb_isStaff ])
        self.db.session.commit()
        self.tabl_entrylist1 = EntryList(table_id=self.table1.id)
        self.tabl_entrylist2 = EntryList(table_id=self.table1.id)
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

    def test_entry_creation(self):
        """
        Test creating an entry based on above tableparameters created above
        """
        with self.app.app_context():
            self.cls_setup()
            

            tb_id_entry1 = Entry(value="1", tableparameter_id=self.Tb_id.id, entry_list_id=self.tabl_entrylist1.id)
            tb_name_entry1 = Entry(value="Peter", tableparameter_id = self.Tb_name.id, entry_list_id=self.tabl_entrylist1.id)
            tb_age_entry1 = Entry(value="20", tableparameter_id=self.Tb_age.id, entry_list_id=self.tabl_entrylist1.id)
            tb_email_entry1 = Entry(value="test@test.com", tableparameter_id=self.Tb_email.id, entry_list_id=self.tabl_entrylist1.id)
            tb_created_entry1 = Entry(value="2024-02-07", tableparameter_id=self.Tb_created, entry_list_id=self.tabl_entrylist1.id)
            tb_isstaff_entry1 = Entry(value="True", tableparameter_id=self.Tb_isStaff, entry_list_id=self.tabl_entrylist1.id)
        
            tb_id_entry2 = Entry(value="2", tableparameter_id=self.Tb_id.id, entry_list_id=self.tabl_entrylist2.id)
            tb_name_entry2 = Entry(value="John", tableparameter_id = self.Tb_name.id, entry_list_id=self.tabl_entrylist2.id)
            tb_age_entry2 = Entry(value="40", tableparameter_id=self.Tb_age.id, entry_list_id=self.tabl_entrylist2.id)
            tb_email_entry2 = Entry(value="test2@test.com", tableparameter_id=self.Tb_email.id, entry_list_id=self.tabl_entrylist2.id)
            tb_created_entry2 = Entry(value="2024-02-07", tableparameter_id=self.Tb_created, entry_list_id=self.tabl_entrylist2.id)
            tb_isstaff_entry2 = Entry(value="False", tableparameter_id=self.Tb_isStaff, entry_list_id=self.tabl_entrylist2.id)


            self.db.session.add_all([
                tb_id_entry1, tb_name_entry1, tb_age_entry1, tb_email_entry1, tb_created_entry1, tb_isstaff_entry1,
                tb_id_entry2, tb_name_entry2, tb_age_entry2, tb_email_entry2, tb_created_entry2, tb_isstaff_entry2,
            ])

            self.assertEqual(len(self.tabl_entrylist1.entries), 6)
            self.assertEqual(len(self.tabl_entrylist2.entries), 6)