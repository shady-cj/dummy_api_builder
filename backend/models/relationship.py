"""
Relationship model to define ForeignKey
relationship
"""
from . import db


entrylist_relationships = db.Table('entrylist_relationships',
                                 db.Column('relationship_id', db.Integer, db.ForeignKey('relationship.id')),
                                 db.Column('entrylist_id', db.Integer, db.ForeignKey('entrylist.id'))
                                 )


class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_ref_pk = db.Column(db.String, nullable=False) # reference to fk pk
    entrylists = db.relationship("EntryList", secondary=entrylist_relationships, backref="relationships")
    fk_rel = db.Column(db.String, nullable=False) # foreign key relationship in form (parentapi.table->childapi.table.field)
    fk_model_name = db.Column(db.String, nullable=False) # e.g users, posts, etc
