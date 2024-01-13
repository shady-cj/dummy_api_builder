from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()
from api.v1.views import app_views
from flask_migrate import Migrate
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET')

app.register_blueprint(app_views)
CORS(app)
from models import db
migrate = Migrate()


@app.route('/')
def index():
    return jsonify({ "message": "Welcome to dummy api"})


