from main import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), unique=True, nullable=False)
    type = db.Column(db.String(), nullable=False, default="Free")
    limit = db.Column(db.Integer, nullable=False, default=2)

    def __init__(self, name, phone_number, type, limit):
        self.name = name
        self.phone_number = phone_number
        self.type = type
        self.limit = limit

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'type': self.type,
            'limit': self.limit
        }


class ClientAccount(db.Model):
    __tablename__ = 'client_account'

    id = db.Column(db.Integer, primary_key=True)
    debtor_name = db.Column(db.String(), nullable=False)
    debtor_phone_number = db.Column(db.String(), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, debtor_name, debtor_phone_number, user_id):
        self.debtor_name = debtor_name
        self.debtor_phone_number = debtor_phone_number
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'debtor_name': self.debtor_name,
            'debtor_phone_number': self.debtor_phone_number,
            'user_id': self.user_id
        }


class AccountData(db.Model):
    __tablename__ = 'data_account'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client_account.id'))

    def __init__(self, amount, date, user_id, client_id):
        self.amount = amount
        self.date = date
        self.user_id = user_id
        self.client_id = client_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date,
            'user_id': self.user_id,
            'client_id': self.client_id
        }
