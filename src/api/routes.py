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
import json
from plaid.model.accounts_get_request import AccountsGetRequest
import os
from plaid.api import plaid_api
import plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest


load_dotenv()

client_id = os.getenv('PLAID_CLIENT_ID')
secret = os.getenv('PLAID_SECRET')
environment = os.getenv('PLAID_ENVIRONMENT')

# Plaid Configuration
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': client_id,
        'secret': secret,
    }
)
api_client = plaid.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

api = Blueprint('api', __name__)
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


@api.route('/create_link_token', methods=['POST'])
def create_link_token():
    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(client_user_id='user.id'),
        client_name='FinanceBuddy',
        products=[Products("transactions"), Products("investments")],
        country_codes=[CountryCode('US')],
        language='en'
    )
    response = plaid_client.link_token_create(request)
    return jsonify(response.to_dict()), 200

# to exchange the public token in order to be able to access the api call
@api.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    global access_token, item_id
    public_token = request.json['public_token']  # Retrieve the public_token from the request body
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=public_token
    )
    try:
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        # You should save the access_token and item_id in a persistent database associated with the user
        return jsonify({'public_token_exchange': 'complete', 'access_token': access_token, 'item_id': item_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# MAKING THE API CALL NOW TO RETRIEVE FIANCIAL DATA:
@api.route('/accounts', methods=['GET'])
def get_accounts():
    # Access the global access_token (or retrieve it from where it's stored)
    global access_token

    try:
        request = AccountsGetRequest(access_token=access_token)
        accounts_response = plaid_client.accounts_get(request)
        return jsonify(accounts_response.to_dict())
    except plaid.ApiException as e:
        response = json.loads(e.body)
        return jsonify({
            'error': {
                'status_code': e.status,
                'display_message': response['error_message'],
                'error_code': response['error_code'],
                'error_type': response['error_type']
            }
        }), 400


