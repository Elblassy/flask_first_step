from main import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phone_number = db.Column(db.String())

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number
        }
