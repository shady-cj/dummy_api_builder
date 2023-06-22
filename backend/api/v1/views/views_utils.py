"""
This module contains series
of helper functions for the existing
views.
"""


def validate_constraint(constraint):
    valid_constraints = [
        "foreign_key",
        "unique",
        "nullable",
        "primary_key"
    ]
    if constraint not in valid_constraints:
        return False
    return True

def validate_dtType(type):
    valid_types = [
        "string",
        "text",
        "integer",
        "boolean",
        "date",
        "datetime"
    ]
    if type not in valid_types:
        return False
    return True


def validate_name(name):
    import keyword
    if not name:
        return False
    if len(name) < 3 or type(name) != str:
        return False
    return name.isidentifier() and not keyword.iskeyword(name)



def validate_entry_value(value, data_type):
    from dateutil.parser import parse
    import datetime
    if not value:
        return False
    value = str(value)
    if data_type == "integer":
        try:
            eval_value = eval(value)
            assert(type(eval_value) == int)
        except:
            return False
    elif data_type == "boolean":
        try:
            eval_value = eval(value)
            assert(type(eval_value) == bool)
        except:
            return False
    elif data_type == "datetime":
        try:
            eval_value = parse(value)
            assert(type(eval_value) == datetime.datetime)
        except:
            return False
    elif data_type == "date":
        try:
            eval_value = parse(value)
            assert(type(eval_value.date()) == datetime.date)
        except:
            return False
    return True


def validate_entry_value_length(value, type, length):
    if not length:
        return True
    if type == 'text' or type == 'string':
        return len(str(value)) <= length
    return True


def validate_entry_constraints(value, tbl_p):
    fk = None
    for const in tbl_p.constraints:
        const = const.name
        if const.name == "nullable":
            if not value:
                return True, "nullable", None
        if const.name == "foreign_key":
            from models.table import Table
            from models.api import Api
            from models.tableparameter import TableParameter
            from models.entrylist import EntryList
            from models.relationship import Relationship
            get_ref_field = tbl_p.foreign_key_reference_field
            api, table = get_ref_field.split(".")
            r_api = Api.query.filter_by(name=api).first()
            if not r_api:
                return False, "fk", "Api referenced by foreign key doesn't exist anymore"
            r_table = Table.query.filter_by(name=table, api_id=r_api.id).first()
            if not r_table:
                return False, "fk", "Table referenced by foreign key doesn't exist anymore"
            # r_field = TableParameter.query.filter_by(name=field, table_id=r_table.id).first()
            # if not r_field:
            #     return False, "fk", "Field referenced by foreign key doesn't exist anymore"
            e_li = EntryList.query.filter_by(table_id=r_table.id, primary_key_value = value).first()
            if not e_li:
                return False, "fk", "Primary key referenced for the foreign key doesn't exist"
            fk = "fk"
        if const.name == "unique":
            from models.entry import Entry
            if Entry.query.filter_by(tableparameter_id=tbl_p.id, value=value).first():
                return False, "uniq", f"{value} already exists in the database. It must be unique"
    return True, fk, None