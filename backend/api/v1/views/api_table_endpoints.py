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
    table_parameters = data.get('tbl_params')

    if not len(table_parameters):
        return jsonify({"error": "table parameters are required"}), 400
    
    
    if not name:
        return jsonify({"error": "name of the model is required"}), 400

    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    
    get_table = Table.query.filter_by(api_id=api_id, name=name).first()

    if get_table:
        return jsonify({"error": "Table already exists"}), 400
    
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
                return jsonify({"error": "name of table param already exist for this table, it must be unique"})
            p = TableParameter(name=param_name, data_type=param_dt, dataType_length=param_dt_length, table_id=new_table.id)
            for const in constraints:
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



@app_views.route('/my_api/<api_id>/update_model/<model_id>', methods=["PUT"])
@login_required
def update_model(user, api_id, model_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    table_parameters = data.get('tbl_params') or []
    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    get_table = Table.query.filter_by(id=model_id, api_id=api_id).first()
    if not get_table:
        return jsonify({"error": "Table doesn't exist"}), 400
    if get_table.entry_lists:
        return jsonify({"error": "You cannot the table when it already has data"}), 400
    if name:
        get_table.name = name
    if description:
        get_table.description = description
    
    for param in table_parameters:
        param_id = param.get("id")
        param_name = param.get("name")
        param_dt = param.get("datatype")
        param_dt_length = param.get("dt_length")
        constraints = param.get("constraints") or []
        if not param_id:
            continue
        try:
            p = TableParameter.query.filter_by(id=param_id, table_id=get_table.id).first()  
            if not p:
                continue
            if param_name:
                if not TableParameter.query.filter_by(name=param_name, table_id=get_table.id).first():
                    p.name = param_name
            if param_dt:
                p.data_type = param_dt
            if param_dt_length:
                p.dataType_length = param_dt_length
            for const in constraints:
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



@app_views.route('/my_api/<api_id>/show_model/<model_id>', methods=["GET"])
@login_required
def show_model(user, api_id, model_id):
    api = Api.query.filter_by(id=api_id, user_id=user.id).first()
    if not api:
        return jsonify({"error": "no api of such is associated to the user"})
    get_table = Table.query.filter_by(id=model_id, api_id=api_id).first()
    if not get_table:
        return jsonify({"error": "Table doesn't exist"}), 400
    tbl_params = []
    for params in get_table.table_parameters:
        tbl_constraints = []
        for const in params.constraints:
            tbl_constraints.append(const.name.value)
        tbl_params.append({
            "id": params.id,
            "name": params.name,
            "data_type": params.data_type.value,
            "datatype_length": params.dataType_length,
            "constraints": tbl_constraints
        })
    
    return jsonify({
        "id": get_table.id, 
        "name": get_table.name,
        "desc": get_table.description,
        "table_params": tbl_params
        })