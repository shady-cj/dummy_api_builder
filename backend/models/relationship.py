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
    entry_ref_pk = db.Column(db.String, nullable=False) # reference to foreign key primary key
    entrylists = db.relationship("EntryList", secondary=entrylist_relationships, backref="relationships")
    fk_rel = db.Column(db.String, nullable=False) # foreign key relationship in form (parentapi.table->childapi.table.field)
    fk_model_name = db.Column(db.String, nullable=False) # e.g <api_name>_<model_name>s (blog_users, blog_posts, etc) api name is added to distiguish apis since foreign key can be mapped to any api created by the user, so this is so to avoid namespace conflict when query the data.
