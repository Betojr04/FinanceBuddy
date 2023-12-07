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
import os
from plaid.api import plaid_api
import plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

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


# the OG create link token
# @api.route('/create_link_token', methods=['POST'])
# def create_link_token():
#     try:
#         print("Creating link token...")
#         request = plaid.LinkTokenCreateRequest(
#             user=plaid.LinkTokenCreateRequestUser(client_user_id='user.id'),
#             client_name='FinanceBuddy',
#             products=[plaid.Products('transactions'), plaid.Products('investments'), 
#                       plaid.Products('liabilities'), plaid.Products('enrich')],
#             country_codes=[plaid.CountryCode('US')],
#             language='en'
#         )
#         response = plaid_client.link_token_create(request)
#         return jsonify(response.to_dict()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



# @api.route("/create_link_token", methods=['POST'])
# def create_link_token():
    
#     user = User.find(...)
#     client_user_id = user.id
  
#     request = LinkTokenCreateRequest(
#             products=[Products("auth"), Products("transactions"),Products("investments"),Products("liabilities"),Products("enrich")],
#             client_name="Plaid Test App",
#             country_codes=[CountryCode('US'), CountryCode('CA')],
#             redirect_uri='https://domainname.com/oauth-page.html',
#             language='en',
#             webhook='https://webhook.example.com',
#             user=LinkTokenCreateRequestUser(
#                 client_user_id=client_user_id
#             )
#         )
#     response = client.link_token_create(request)
    
#     return jsonify(response.to_dict())

@api.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    try:
        public_token = request.json.get('public_token')
        if not public_token:
            return jsonify({'error': 'Missing public token'}), 400

        exchange_request = plaid.ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        # Here you can store the access_token in your database associated with the user
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



