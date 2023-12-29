"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User, TransactionCursor, Transaction
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import datetime
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

from plaid.model.transactions_sync_request import TransactionsSyncRequest





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


"""
ROUTE FOR GETTING ACCOUNTS
"""
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



"""
HELPER FUNCTION FOR TRANSACTION SYNC
"""
def sync_transactions_with_plaid(access_token, cursor):
    added = []
    modified = []
    removed = []
    has_more = True

    while has_more:
        request = TransactionsSyncRequest(
            access_token=access_token,
            cursor=cursor,
        )
        response = plaid_client.transactions_sync(request)

        added.extend(response['added'])
        modified.extend(response['modified'])
        removed.extend(response['removed'])

        has_more = response['has_more']
        cursor = response['next_cursor']

    return added, modified, removed, cursor

"""
ROUTE FOR TRANSACTION SYNC
"""
@api.route('/sync_transactions', methods=['GET'])
@jwt_required()
def sync_transactions():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if not user or not user.plaid_access_token:
        return jsonify({'error': 'Access token or item not found'}), 404

    try:
        cursor = get_latest_cursor_or_none(user.plaid_item_id)
        added, modified, removed, new_cursor = sync_transactions_with_plaid(plaid_client, user.plaid_access_token, cursor)

        apply_updates(user.plaid_item_id, added, modified, removed, new_cursor)
        return jsonify({'message': 'Transactions synced successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""
ALL THESE ARE RELATED TO THE TRANSACTION SYNC REQUEST
"""
def get_latest_cursor_or_none(item_id):
    # Assuming you have a model named 'TransactionCursor' that stores your cursors
    cursor_record = TransactionCursor.query.filter_by(item_id=item_id).order_by(TransactionCursor.created_at.desc()).first()
    return cursor_record.cursor if cursor_record else None

def apply_updates(item_id, added, modified, removed, cursor):
    # Handle added transactions
    for transaction in added:
        new_transaction = Transaction(transaction_id=transaction['transaction_id'], item_id=item_id, **transaction)
        db.session.add(new_transaction)

    # Handle modified transactions
    for transaction in modified:
        Transaction.query.filter_by(transaction_id=transaction['transaction_id']).update(transaction)

    # Handle removed transactions
    for transaction_id in removed:
        Transaction.query.filter_by(transaction_id=transaction_id).delete()

    # Update the cursor
    new_cursor = TransactionCursor(item_id=item_id, cursor=cursor)
    db.session.add(new_cursor)

    db.session.commit()





