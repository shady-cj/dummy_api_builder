"""
Defining routes for performing crud operations on
tables/model in an api
"""

from api.v1.views import app_views
from flask import request, jsonify
from api.v1.auth.auth import login_required
from models import db
from models.api import Api
from models.table import Table
from models.tableparameter import TableParameter
from models.constraints import Constraint
from .views_utils import validate_dtType, validate_constraint, validate_name

"""
We won't be implementing a table/model list endpoint
as it would have been added with api_list
"""


@app_views.route('/my_api/<api_id>/create_model', methods=["POST"])
@login_required
def create_model(user, api_id):
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    table_parameters = data.get('tbl_params') or []
    print(data)

    if type(table_parameters) != list and not len(table_parameters):
        return jsonify({"error": "table parameters are required"}), 400
    
    if not name:
        return jsonify({"error": "name of the model is required"}), 400

    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    
    get_table = Table.query.filter_by(api_id=api_id, name=name).first()

    if get_table:
        return jsonify({"error": "Table already exists"}), 400
    if not validate_name(name):
        return jsonify({"error": "Table name must be a valid python identifier, not a python keyword and must be atleast 3 letters"}), 400
    new_table = Table(name=name, description=description, api_id=api_id)
    db.session.add(new_table)
    db.session.commit()
    for param in table_parameters:
        param_name = param.get("name")
        param_dt = param.get("datatype")
        param_dt_length = param.get("dt_length")
        constraints = param.get("constraints") or []
        try:
            if TableParameter.query.filter_by(name=param_name, table_id=new_table.id).first():
                return jsonify({"error": "name of table parameter already exist for this table, it must be unique"}), 400
            if not validate_dtType(param_dt):
                return jsonify({"error": "invalid data type"}), 400
            if not validate_name(param_name):
                return jsonify({"error": "invalid name(must be a valid python identifier) and not a python keyword"}), 400
            try:
                if param_dt_length:
                    param_dt_length = int(param_dt_length) or None
            except ValueError:
                return jsonify({"error": "invalid data type length"})
            p = TableParameter(name=param_name, data_type=param_dt, dataType_length=param_dt_length, table_id=new_table.id)
            for const in constraints:
                if not validate_constraint(const):
                    return jsonify({"error": "invalid constraint"}), 400
                if const == "foreign_key":
                    fk_rf = param.get("foreign_key_rf") #expected format(api.table.field)
                    if not fk_rf:
                        return jsonify({"error": "Expected a foreign key reference field."}), 400
                    f_api, f_table, field = fk_rf.split(".")
                    r_api = Api.query.filter_by(name=f_api, user_id=user.id).first()
                    if not r_api:
                        return jsonify({"error": "Api name referenced in the foreign key doesn't exist"}), 400
                    r_table = Table.query.filter_by(name=f_table, api_id=r_api.id).first()
                    if not r_table:
                        return jsonify({"error", "Table name referenced doesn't exist"}), 400
                    r_field = TableParameter.query.filter_by(name=field, table_id=r_table.id).first()
                    if not r_field:
                        return jsonify({"error": "Field name referenced doesn't exist"}), 400
                    p.foreign_key_reference_field = fk_rf
                if const == "primary_key":
                    p.primary_key = True
                
                get_c = Constraint.query.filter_by(name=const).first()
                if get_c:
                    p.constraints.append(get_c)
                else:
                    p.constraints.append(Constraint(name=const))
            db.session.add(p)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong"}), 400
    db.session.commit()
    return jsonify({"id": new_table.id, "name": new_table.name, "desc": new_table.description})



@app_views.route('/my_api/<api_id>/update_model/<model_name>', methods=["PUT"])
@login_required
def update_model(user, api_id, model_name):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    table_parameters = data.get('tbl_params') or []
    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    get_table = Table.query.filter_by(name=model_name, api_id=api_id).first()
    if not get_table:
        return jsonify({"error": "Table doesn't exist"}), 400
    if get_table.entry_lists:
        return jsonify({"error": "You cannot the table when it already has data"}), 400
    if type(table_parameters) != list:
        return jsonify({"error": "table_parameter must be a list"}), 400
    if name and validate_name(name):
        get_table.name = name
    if description:
        get_table.description = description
    
    for param in table_parameters:
        param_name = param.get("name")
        param_dt = param.get("datatype")
        param_dt_length = param.get("dt_length")
        constraints = param.get("constraints") or []
        if not param_name:
            continue
        try:
            p = TableParameter.query.filter_by(name=param_name, table_id=get_table.id).first()  
            if not p:
                if validate_name(param_name) and param_dt and validate_dtType(param_dt):
                    p = TableParameter(name=param_name, table_id=get_table.id, data_type=param_dt)
                else:
                    continue
            else:        
                if validate_name(param_name):
                    p.name = param_name
                if param_dt:
                    if validate_dtType(param_dt):
                        p.data_type = param_dt
            if param_dt_length:
                try:
                    param_dt_length = int(param_dt_length)
                    p.dataType_length = param_dt_length
                except ValueError:
                    pass
            for const in constraints:
                if not validate_constraint(const):
                    continue
                if const == "foreign_key":
                    fk_rf = param.get("foreign_key_rf") #expected format(api.table.field) 
                    if not fk_rf:
                        continue
                    f_api, f_table, field = fk_rf.split(".")
                    r_api = Api.query.filter_by(name=f_api, user_id=user.id).first()
                    if not r_api:
                        continue
                    r_table = Table.query.filter_by(name=f_table, api_id=r_api.id).first()
                    if not r_table:
                        continue
                    r_field = TableParameter.query.filter_by(name=field, table_id=r_table.id).first()
                    if not r_field:
                        continue
                    p.foreign_key_reference_field = fk_rf
                if const == "primary_key":
                    p.primary_key = True
                
                get_c = Constraint.query.filter_by(name=const).first()
                if get_c:
                    p.constraints.append(get_c)
                else:
                    p.constraints.append(Constraint(name=const))
            db.session.add(p)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong"}), 400
    db.session.commit()
    return jsonify({"id": get_table.id, "name": get_table.name, "desc": get_table.description})



@app_views.route('/my_api/<api_id>/show_model/<model_name>', methods=["GET"])
@login_required
def show_model(user, api_id, model_name):
    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    get_table = Table.query.filter_by(name=model_name, api_id=api_id).first()
    if not get_table:
        return jsonify({"error": "Table doesn't exist"}), 400
    tbl_params = []
    for params in get_table.table_parameters:
        tbl_constraints = []
        for const in params.constraints:
            tbl_constraints.append(const.name.value)
        tbl_params.append({
            "index": params.id,
            "name": params.name,
            "datatype": params.data_type.value,
            "dt_length": params.dataType_length,
            "constraints": tbl_constraints
        })
    
    return jsonify({
        "id": get_table.id, 
        "name": get_table.name,
        "desc": get_table.description,
        "table_params": tbl_params
        })



@app_views.route('/my_api/<api_id>/delete_model/<model_name>', methods=["DELETE"])
@login_required
def delete_model(user, api_id, model_name):
    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    Table.query.filter_by(name=model_name, api_id=api_id).delete()
    db.session.commit()
    return jsonify(''), 204