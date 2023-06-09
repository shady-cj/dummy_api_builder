"""
Creating constraints table with a many to many
relationship to table_parameters
"""

from . import db
import enum


class ValidConstraints(enum.Enum):
    foreign_key = 'ForeignKey'
    unique = 'unique'
    nullable = 'nullable'
    primarykey = 'primarykey'

class Constraint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(ValidConstraints), default=ValidConstraints.nullable, nullable=False, unique=True)