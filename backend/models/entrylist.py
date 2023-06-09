"""
Defining the model for entry lists
e.g
name: peter
age: 15
e.t.c..
"""
from . import db


class EntryList(db.Model):
    __tablename__ = 'entrylist'
    id = db.Column(db.Integer, primary_key=True)
    primary_key_value = db.Column(db.Text, nullable=False, unique=True)
    entries = db.relationship('Entry', back_populates='entry_list')
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    table = db.relationship('Table', back_populates='entry_lists')