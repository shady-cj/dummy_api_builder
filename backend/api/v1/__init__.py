
from flask import Flask
import os
def create_app(env=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Test.db' if env == "test" else 'sqlite:///Database.db'
    if env == "test":
        app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET')
    return app