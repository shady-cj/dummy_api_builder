"""
Define all user's authentication routes here
"""
from api.v1.views import app_views
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from api.v1.auth.auth import login_required
from models import db, User
import jwt


@app_views.route('/signup', methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if not all([email, password, confirm_password]):
        return jsonify({'error': 'email, password, confirm_password fields are all required'}), 400
    if len(password) < 8 or password != confirm_password:
        return jsonify({"error": "Password validation failed"}), 400
    user = User.query.filter_by(email = email).first()
    if user:
        return make_response('Account already exists, please login', 202)
    hash_password = generate_password_hash(password)
    api_token = f'{str(uuid.uuid4())}-{str(uuid.uuid4())}'
    user = User(email=email, password=hash_password, api_token=api_token)
    db.session.add(user)
    db.session.commit()
    return make_response('Account registered successfully', 201)


@app_views.route('/login', methods=["POST"])
def login():
    credentials = request.get_json()
    email = credentials.get('email')
    password = credentials.get('password')

    if not all([email, password]):
        return jsonify({'error': 'email and password fields are required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Incorrect email or password'}), 400
    if check_password_hash(user.password, password):
        # Generates new public_id after every login

        while True:
            # Ensuring public_id is unique before updating
            new_public_id = str(uuid.uuid4())
            check_associated_public_id = User.query.filter_by(public_id = new_public_id).first()
            if not check_associated_public_id:
                break
        
        from api.v1.app import app
        user.public_id = new_public_id
        db.session.commit()

        # Create jwt token
        token = jwt.encode({
            'public_id': new_public_id,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')}), 200
    return jsonify({'error': 'Incorrect email or password'}), 400


@app_views.route('/me')
@login_required
def get_me(user):
    details = {
        "email": user.email,
        "api_token": user.api_token
    }
    return jsonify(details), 200


@app_views.route('/logout', methods=['POST'])
@login_required
def logout(user):
    user.public_id = None
    db.session.commit()
    return make_response('Logged out', 200)