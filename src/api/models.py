from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

"""
USER DATA MODEL
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    plaid_access_token = db.Column(db.String(200))
    plaid_item_id = db.Column(db.String(200))
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

"""
TRANSACTION DATA MODEL
"""
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transaction_id = db.Column(db.String(100), unique=True)
    amount = db.Column(db.Float)
    date = db.Column(db.Date)

"""
TRANSACTION CURSOR MODEL
"""
class TransactionCursor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(100))
    cursor = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

