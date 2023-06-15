"""
Creating entries in the table:
e.g name="peter"
age=12
etc..
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from api.v1.auth.auth import login_required
from models import db
from models.api import Api
from models.table import Table
from models.user import User
from models.tableparameter import TableParameter
from models.constraints import Constraint
from models.entry import Entry
from models.entrylist import EntryList
from models.relationship import Relationship
from .views_utils import validate_entry_constraints, validate_entry_value_length, validate_entry_value

@app_views.route('<api_token>/my_api/<api_name>/model/<model_name>/', methods=["GET", "POST"])
def add_entry(api_token, api_name, model_name):
    user = User.query.filter_by(api_token=api_token).first()
    if not user:
        return make_response("invalid token", 401)
    api = Api.query.filter_by(name=api_name, user_id=user.id).first()
    if not api:
        return make_response(f"{api_name} does not exists in the users catalog", 400)
    table = Table.query.filter_by(name=model_name, api_id=api.id).first()
    if not table:
        return make_response(f"model {model_name} doesn't exist in the api", 400)
    if request.method == "POST":
        data = request.get_json()
        entries = data.get("entries") or []
        e_list = EntryList(table_id = table.id)
        db.session.add(e_list)
        db.session.commit()
        checkpoint = db.session.begin_nested()
        primary_keys = []
        for entry in entries:
            entry_name = entry.get("name")
            entry_value = entry.get("value")
            rel_key = f"{tbl_p.foreign_key_reference_field}->{api.name}.{table.name}.{entry_name}" # incase of foreign key
            tbl_p = TableParameter.query.filter_by(name=entry_name, table_id=table.id)
            if not tbl_p:
                EntryList.query.filter_by(id=e_list.id).delete()
                checkpoint.rollback()
                return jsonify({"error": "such model name doesn't exist"}), 400
            stat, const_type, err_msg = validate_entry_constraints(entry_value, tbl_p)
            if const_type == "nullable" and stat:
                continue
            if not stat and const_type == "uniq":
                EntryList.query.filter_by(id=e_list.id).delete()
                checkpoint.rollback()
                return jsonify({"error": err_msg}), 400
            if not stat and const_type == "fk":
                EntryList.query.filter_by(id=e_list.id).delete()
                checkpoint.rollback()
                Relationship.query.filter_by(fk_rel=rel_key).delete()
                return jsonify({"error": err_msg}), 400
            if not validate_entry_value(entry_value, tbl_p.data_type.name):
                EntryList.query.filter_by(id=e_list.id).delete()
                checkpoint.rollback()
                return jsonify({"error": "Wrong data type passed."}), 400
            if not validate_entry_value_length(entry_value, tbl_p.data_type.name, tbl_p.dataType_length):
                EntryList.query.filter_by(id=e_list.id).delete()
                checkpoint.rollback()
                return jsonify({"error": "max length of data exceeded"})
            if tbl_p.primary_key:
                primary_keys.append({"id": tbl_p.id, "value": entry_value})
            e = Entry(value=entry_value, tableparameter_id=tbl_p.id, entry_list_id=e_list.id)
            if const_type == "fk":
                relationship = Relationship.query.filter_by(fk_rel = rel_key, entry_id = entry_value, fk_model_name=f"{table.lower()}s").first()
                if relationship:
                    relationship.entrylists.append(e_list)
                else:
                    try:
                        relationship = Relationship(entry_id=entry_value, fk_rel=rel_key, fk_model_name=f"{table.lower()}s")
                        relationship.entrylists.append(e_list)
                        db.session.add(relationship)
                    except:
                        EntryList.query.filter_by(id=e_list.id).delete()
                        checkpoint.rollback()
                        return jsonify({"error": "Could not reference the foreign key id"}), 400
            db.session.add(e)
        primary_keys_sorted = sorted(primary_keys, key=lambda x: x["id"])
        primary_key_value = "".join([ str(key["value"]) for key in primary_keys_sorted])
        # check if primary key already exists
        if EntryList.query.filter_by(table_id=table.id, primary_key_value=primary_key_value).first():
            checkpoint.rollback()
            EntryList.query.filter_by(id=e_list.id).delete()
            return jsonify({"error": "Primary key already exist"}), 400
        
        e_list.primary_key_value = primary_key_value
        db.session.commit()
        return jsonify({"message": "Entry Created"}), 201
