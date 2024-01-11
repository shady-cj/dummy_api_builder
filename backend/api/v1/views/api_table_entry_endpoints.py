"""
Creating entries in the table:
e.g name="peter"
age=12
etc..
"""
from dateutil.parser import parse
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

@app_views.route('<api_token>/my_api/<api_name>/model/<model_name>', methods=["GET", "POST"])
def add_list_entry(api_token, api_name, model_name):
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
        entries = data.get("entries") or {}
        if type(entries) != dict: 
            return jsonify({"error": "Entries must be an object"}), 400
        # This logic would be refactored. 
        required_parameters = 0
        for table_parameter in table.table_parameters:
            current_constraint = [c.name.value for c in table_parameter.constraints]
            if "nullable" in current_constraint:
                continue
            required_parameters += 1
        # The check is done to ensure the user is passing all required fields and no none declared field is passed
        # The current check just compares the length, more validation is done later on below
        if len(entries) < required_parameters or len(entries) > len(table.table_parameters):
            return jsonify({"error": "Incomplete field or a non declared field has been passed"}), 400
        e_list = EntryList(table_id = table.id)
        db.session.add(e_list)
        db.session.commit()
        checkpoint = db.session.begin_nested()
        primary_keys = [] # You can have multiple primary keys on a table

        """
        entries format 
        [
        {
        "name": "Name",
        "value": "Peter"
        }, ...
        ]
        """
        for entry_name, entry_value in entries.items():
            tbl_p = TableParameter.query.filter_by(name=entry_name, table_id=table.id).first()
            if not tbl_p:
                checkpoint.rollback()
                EntryList.query.filter_by(id=e_list.id).delete()
                db.session.commit()
                return jsonify({"error": f"such field name {entry_name} doesn't exist"}), 400
            rel_key = f"{tbl_p.foreign_key_reference_field}->{api.name}.{table.name}.{entry_name}" # incase of foreign key
            stat, const_type, err_msg = validate_entry_constraints(entry_value, tbl_p, user) # Validating the entry against the existing constraint
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
                if not err_msg.startswith('Primary key'):
                    Relationship.query.filter_by(fk_rel=rel_key).delete()
                else:
                    rel = Relationship.query.filter_by(fk_rel=rel_key, entry_ref_pk=entry_value).first()  # check if relationship already has a field referencing the foreign key
                    if rel:
                        rel.entrylists.clear() # remove all relationships associated
                        Relationship.query.filter_by(fk_rel=rel_key, entry_ref_pk=entry_value).delete()  # Then delete the relationship
                db.session.commit()
                return jsonify({"error": err_msg}), 400
            if not const_type == "fk" and not validate_entry_value(entry_value, tbl_p.data_type.name):
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
            if tbl_p.data_type.name == "datetime":
                parsed_value = parse(entry_value)
                entry_value = parsed_value
            if tbl_p.data_type.name == "date":
                parsed_value = parse(entry_value)
                entry_value = parsed_value.date()
            e = Entry(value=entry_value, tableparameter_id=tbl_p.id, entry_list_id=e_list.id)
            foreignKey_model_name = f"{api.name.lower()}_{table.name.lower()}s"
            if const_type == "fk":
                relationship = Relationship.query.filter_by(fk_rel = rel_key, entry_ref_pk = entry_value, fk_model_name=foreignKey_model_name).first()
                if relationship:
                    relationship.entrylists.append(e_list)
                else:
                    try:
                        relationship = Relationship(entry_ref_pk=entry_value, fk_rel=rel_key, fk_model_name=foreignKey_model_name)
                        relationship.entrylists.append(e_list)
                        db.session.add(relationship)
                    except:
                        checkpoint.rollback()
                        EntryList.query.filter_by(id=e_list.id).delete()
                        db.session.commit()
                        return jsonify({"error": "Could not reference the foreign key id"}), 400
            db.session.add(e)
        if not primary_keys:
            return jsonify({"error", "No primary key value"}),400
        

        # Merge all the primary keys to form the main primary key for the field.
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
                    if entry.tableparameter.data_type.name == "integer":
                        e_value = int(entry.value)
                    else:
                        e_value = entry.value
                    if tp_name in args:
                        found_valid_arg = True
                        if args[tp_name] == entry.value:
                            filter_in = True
                    entry_data[tp_name] = e_value
                if filter_in:
                    data.append(entry_data)
            if not found_valid_arg: # if none was valid then just return all
                data = []
                for entry_list in table.entry_lists:
                    if entry_list.entries:
                        data.append({entry.tableparameter.name: int(entry.value) if entry.tableparameter.data_type.name == "integer" else entry.value for entry in entry_list.entries})
        else:
            for entry_list in table.entry_lists:
                if entry_list.entries:
                    data.append({entry.tableparameter.name: int(entry.value) if entry.tableparameter.data_type.name == "integer" else entry.value for entry in entry_list.entries})
        return jsonify(data), 200



@app_views.route('<api_token>/my_api/<api_name>/model/<model_name>/<model_id>', methods=["PUT", "GET", "DELETE"])
def update_delete_retrieve_entry(api_token, api_name, model_name, model_id):
    user = User.query.filter_by(api_token=api_token).first()
    if not user:
        return make_response("invalid api id", 401)
    api = Api.query.filter_by(name=api_name, user_id=user.id).first()
    if not api:
        return make_response(f"{api_name} does not exists in the users catalog", 400)
    table = Table.query.filter_by(name=model_name, api_id=api.id).first()
    if not table:
        return make_response(f"model {model_name} doesn't exist in the api", 400)
    e_list = EntryList.query.filter_by(table_id = table.id, primary_key_value = model_id).first()
    if not e_list:
            return jsonify({"error": "primary key value doesn't match any"}), 400
    if request.method == "PUT":
        data = request.get_json()
        entries = data.get("entries") or {}
        # if type(entries) != list or len(entries) != len(table.table_parameters):
        #     return jsonify({"error": "Incomplete fields for the model and entries must be a list"}), 400
        # for e  in Entry.query.filter_by(entry_list_id=e_list.id).all()
        if type(entries) != dict:
            return jsonify({"error": "Entries must be an object"})
        checkpoint = db.session.begin_nested()
        primary_keys = []
        for entry_name, entry_value in entries.items():
            tbl_p = TableParameter.query.filter_by(name=entry_name, table_id=table.id).first()
            if not tbl_p:
                continue
            rel_key = f"{tbl_p.foreign_key_reference_field}->{api.name}.{table.name}.{entry_name}" # incase of foreign key
            stat, const_type, err_msg = validate_entry_constraints(entry_value, tbl_p, user)
            if const_type == "nullable" and stat:
                continue
            if not stat and const_type == "uniq":
                continue
            if not stat and const_type == "fk":
                if not err_msg.startswith('Primary key'):
                    Relationship.query.filter_by(fk_rel=rel_key).delete()
                else:
                    rel = Relationship.query.filter_by(fk_rel=rel_key, entry_ref_pk=entry_value).first()  # check if relationship already has a field referencing the foreign key
                    if rel:
                        rel.entrylists.clear() # remove all relationships associated
                        Relationship.query.filter_by(fk_rel=rel_key, entry_ref_pk=entry_value).delete()  # Then delete the relationship
                db.session.commit()
                continue
            if not const_type == "fk" and not validate_entry_value(entry_value, tbl_p.data_type.name):
                continue
            if not validate_entry_value_length(entry_value, tbl_p.data_type.name, tbl_p.dataType_length):
                continue
            if tbl_p.primary_key:
                primary_keys.append({"id": tbl_p.id, "value": entry_value})
            if tbl_p.data_type.name == "datetime":
                parsed_value = parse(entry_value)
                entry_value = parsed_value
            if tbl_p.data_type.name == "date":
                parsed_value = parse(entry_value)
                entry_value = parsed_value.date()
            e = Entry.query.filter_by(tableparameter_id=tbl_p.id, entry_list_id=e_list.id).first() # Grab the entry to be updated
            foreignKey_model_name = f"{api.name.lower()}_{table.name.lower()}s"
            if e:
                # If the entry exists update the value
                relationship = Relationship.query.filter_by(fk_rel = rel_key, entry_ref_pk = e.value, fk_model_name=foreignKey_model_name).first() 
                # remove the previous value from the relationship before updating it
                if relationship:
                    relationship.entrylists.remove(e_list)
                e.value = entry_value 
            else:
                # in the event where there is no entry (as a result of previous nullable constraints)
                e = Entry(value=entry_value, tableparameter_id=tbl_p.id, entry_list_id=e_list.id)
            if const_type == "fk":
                relationship = Relationship.query.filter_by(fk_rel = rel_key, entry_ref_pk = entry_value, fk_model_name=foreignKey_model_name).first()
                if relationship:
                    relationship.entrylists.append(e_list)
                else:
                    try:
                        relationship = Relationship(entry_ref_pk=entry_value, fk_rel=rel_key, fk_model_name=foreignKey_model_name)
                        relationship.entrylists.append(e_list)
                        db.session.add(relationship)
                    except:
                        continue
            db.session.add(e)
        if primary_keys:
            primary_keys_sorted = sorted(primary_keys, key=lambda x: x["id"])
            primary_key_value = "".join([ str(key["value"]) for key in primary_keys_sorted])
            # check if primary key already exists
            if EntryList.query.filter_by(table_id=table.id, primary_key_value=primary_key_value).first():
                checkpoint.rollback()
                return jsonify({"error": "Primary key already exist"}), 400
            e_list.primary_key_value = primary_key_value
        db.session.commit()
        e_data = {entry.tableparameter.name: entry.value for entry in e_list.entries}            
        return jsonify(e_data), 200
    
    if request.method == "DELETE":
        Entry.query.filter_by(entry_list_id=e_list.id).delete()
        get_rel = Relationship.query.filter(Relationship.entry_ref_pk==e_list.primary_key_value, Relationship.fk_rel.startswith(f"{api_name}.{model_name}")).first()
        if get_rel:
            get_rel.entrylists.clear()
        Relationship.query.filter(Relationship.entry_ref_pk==e_list.primary_key_value, Relationship.fk_rel.startswith(f"{api_name}.{model_name}")).delete()
        EntryList.query.filter_by(table_id = table.id, primary_key_value = model_id).delete()
        db.session.commit()
        return jsonify({'message': 'Entry succesfully deleted'}), 204 # NO content afterall

    if request.method == "GET":
        data = {}
        for data_entry in e_list.entries:
            fieldName = data_entry.tableparameter.name
            data[fieldName] = int(data_entry.value) if data_entry.tableparameter.data_type.name == "integer" else data_entry.value
        tableKeyName = f"{api_name}.{model_name}"
        # rel_key = db.session(Relationship).filter(Relationship.fk_rel.like(f"{tableKeyName}%"), Relationship.entry_ref_pk=e_list.primary_key_value).first()
        rels = Relationship.query.filter(Relationship.fk_rel.startswith(f"{tableKeyName}"), Relationship.entry_ref_pk==e_list.primary_key_value)
        rel_key_data = {} # format {"posts":[..]}
        for rel in rels:
            rel_key_data[rel.fk_model_name] = []
            for e_list_rel in rel.entrylists:
                rel_data = {}
                for ent in e_list_rel.entries:
                    rel_data[ent.tableparameter.name] = int(ent.value) if ent.tableparameter.data_type.name == "integer" else ent.value
                rel_key_data[rel.fk_model_name].append(rel_data)
        data["relationships"] = rel_key_data
        return jsonify(data), 200
