from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()
from api.v1.views import app_views
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET')

app.register_blueprint(app_views)
CORS(app)

@app.route('/')
def index():
    return jsonify({ "message": "Welcome to dummy api"})


if __name__ == "__main__":
    from models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=5900, debug=True)