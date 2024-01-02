"""
Defining model to hold fields for each
tables

This allows the user to define something like this

Name = db.Column(db.String)
Age = db.Column(db.Integer)
_Id = db.Column(db.Integer, primary_key=True)
"""
from . import db
import enum



parameter_constraints = db.Table('parameter_constraint',
                                 db.Column('tableparameter_id', db.Integer, db.ForeignKey('tableparameter.id')),
                                 db.Column('constraint_id', db.Integer, db.ForeignKey('constraint.id'))
                                 )
    

class DataTypes(enum.Enum):
    string = 'String'
    text = 'Text'
    integer = 'Integer'
    boolean = 'Boolean'
    date = 'date'
    datetime = 'datetime'



class TableParameter(db.Model):
    __tablename__ = 'tableparameter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    data_type = db.Column(db.Enum(DataTypes), default=DataTypes.string, nullable=False)
    primary_key = db.Column(db.Boolean, default=False)
    foreign_key_reference_field = db.Column(db.String, nullable=True) # reference table. format "api.table"
    dataType_length = db.Column(db.Integer, nullable=True) # Only valid for strings, text, integers
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    table = db.relationship('Table', back_populates='table_parameters')
    constraints = db.relationship('Constraint', secondary=parameter_constraints, backref='table_parameters', cascade="all, delete")
    entries = db.relationship('Entry', back_populates='tableparameter', cascade="all, delete")


    # Add default values