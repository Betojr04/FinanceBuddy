"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
load_dotenv() 

import os
client_id = os.getenv('PLAID_CLIENT_ID')
secret = os.getenv('PLAID_SECRET')
environment = os.getenv('PLAID_ENVIRONMENT')

from plaid import Client



api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# PLAID CONFIGURATION
client = Client(client_id=client_id, secret=secret, environment=environment)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# REGISTERING A NEW USER
@api.route("/register", methods=['POST'])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


# LOGGING A REGISTERED USER
@api.route("/login", methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # basic validation for email and password
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid email or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200



# CREATING THE LINK TOKEN REQUIRED TO OPEN PLAID LINK ON FRONTEND
@api.route('/create_link_token', methods=['POST'])
def create_link_token():
    response = client.LinkToken.create({
        'user': {
            'client_user_id': 'user_id',  
        },
        'client_name': 'FinanceBuddy',
        'products': ['transactions', 'investments', 'liabilities', 'enrich' ],
        'country_codes': ['US'],
        'language': 'en',
    })
    return response

# THIS RECIVES THE LINK TOKEN CREATED AND TURNS INTO AN ACCESS TOKEN TO USE PLAID SERVICE
@api.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    try:
        public_token = request.json.get('public_token')
        if not public_token:
            return jsonify({'error': 'Missing public token'}), 400

        exchange_response = client.Item.public_token.exchange(public_token)
        access_token = exchange_response['access_token']
        # Store this access_token securely
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


