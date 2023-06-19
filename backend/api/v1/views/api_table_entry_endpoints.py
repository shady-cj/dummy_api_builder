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
        if type(entries) != list or len(entries) != len(table.table_parameters):
            return jsonify({"error": "Incomplete fields for the model"}), 400
        e_list = EntryList(table_id = table.id)
        db.session.add(e_list)
        db.session.commit()
        checkpoint = db.session.begin_nested()
        primary_keys = []
        for entry in entries:
            entry_name = entry.get("name")
            entry_value = entry.get("value")
            tbl_p = TableParameter.query.filter_by(name=entry_name, table_id=table.id).first()
            if not tbl_p:
                checkpoint.rollback()
                EntryList.query.filter_by(id=e_list.id).delete()
                db.session.commit()
                return jsonify({"error": "such model name doesn't exist"}), 400
            rel_key = f"{tbl_p.foreign_key_reference_field}->{api.name}.{table.name}.{entry_name}" # incase of foreign key
            stat, const_type, err_msg = validate_entry_constraints(entry_value, tbl_p)
            if const_type == "nullable" and stat:
                continue
            if not stat and const_type == "uniq":
                checkpoint.rollback()
                EntryList.query.filter_by(id=e_list.id).delete()
                db.session.commit()
                return jsonify({"error": err_msg}), 400
            if not stat and const_type == "fk":
                checkpoint.rollback()
                EntryList.query.filter_by(id=e_list.id).delete()
                Relationship.query.filter_by(fk_rel=rel_key).delete()
                db.session.commit()
                return jsonify({"error": err_msg}), 400
            if not validate_entry_value(entry_value, tbl_p.data_type.name):
                checkpoint.rollback()
                EntryList.query.filter_by(id=e_list.id).delete()
                db.session.commit()
                return jsonify({"error": "Wrong data type passed."}), 400
            if not validate_entry_value_length(entry_value, tbl_p.data_type.name, tbl_p.dataType_length):
                checkpoint.rollback()
                EntryList.query.filter_by(id=e_list.id).delete()
                db.session.commit()
                return jsonify({"error": f"max length of '{entry_name}' exceeded"}), 400
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
                        checkpoint.rollback()
                        EntryList.query.filter_by(id=e_list.id).delete()
                        db.session.commit()
                        return jsonify({"error": "Could not reference the foreign key id"}), 400
            db.session.add(e)
        primary_keys_sorted = sorted(primary_keys, key=lambda x: x["id"])
        primary_key_value = "".join([ str(key["value"]) for key in primary_keys_sorted])
        # check if primary key already exists
        if EntryList.query.filter_by(table_id=table.id, primary_key_value=primary_key_value).first():
            checkpoint.rollback()
            EntryList.query.filter_by(id=e_list.id).delete()
            db.session.commit()
            return jsonify({"error": "Primary key already exist"}), 400
        
        e_list.primary_key_value = primary_key_value
        db.session.commit()
        e_data = {entry.tableparameter.name: entry.value for entry in e_list.entries}            
        return jsonify(e_data), 201
    
    elif request.method == "GET":
        args = dict(request.args)
        data = []
        if args:
            found_valid_arg = False # if params passed in are valid or not
            get_entryLists = EntryList.query.filter_by(table_id=table.id)
            for entry_list in get_entryLists:
                entry_data = {}
                get_entries = Entry.query.filter_by(entry_list_id=entry_list.id)
                filter_in = False
                for entry in get_entries:
                    tp_name = entry.tableparameter.name
                    if tp_name in args:
                        found_valid_arg = True
                        if args[tp_name] == entry.value:
                            filter_in = True
                    entry_data[tp_name] = entry.value
                if filter_in:
                    data.append(entry_data)
            if not found_valid_arg: # if none was valid then just return all
                data = []
                for entry_list in table.entry_lists:
                    if entry_list.entries:
                        data.append({entry.tableparameter.name: entry.value for entry in entry_list.entries})
        else:
            for entry_list in table.entry_lists:
                if entry_list.entries:
                    data.append({entry.tableparameter.name: entry.value for entry in entry_list.entries})
        return jsonify(data), 200
