"""
Defining blueprints for the views
"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from .authentication import *
from .user_api_endpoints import *
from .api_table_endpoints import *
from .api_table_entry_endpoints import *