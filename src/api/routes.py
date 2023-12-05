"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from werkzeug.security import generate_password_hash
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


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

    # basic validation for email || password
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

        # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409

        # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user instance
    new_user = User(email=email, password=hashed_password)

    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201

# LOGGING A REGISTERED USER