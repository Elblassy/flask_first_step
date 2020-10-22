from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User, UserAccount


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/signup", methods=['POST'])
def sign_up():
    if request.data:
        content = request.json
        name = content['name']
        phone_number = content['phone_number']
        try:
            user = User(
                name=name,
                phone_number=phone_number
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(user.serialize()), 201
        except Exception as e:
            return jsonify({'Error': e}), 401
    else:
        return jsonify({'Error': 'please input correct data'}), 400


@app.route("/signin", methods=['POST'])
def sign_in():
    if request.data:
        content = request.json
        phone_number = content['phone_number']
        query = db.session.query(User).filter(User.phone_number == phone_number)
        result = query.first()
        if result:
            return jsonify({"message": "user exist"}), 200
        else:
            return jsonify({"message": "user not exist"}), 401
    else:
        return jsonify({'Error': 'please input correct data'}), 400


@app.route("/get-users", methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users]), 200
    except Exception as e:
        return str(e), 401


@app.route("/add-user-account", methods=['POST'])
def add_client_account():
    if request.data:
        content = request.json
        debtor_name = content['debtor_name']
        debtor_phone_number = content['debtor_phone_number']
        amount = content['amount']
        user_id = content['user_id']
        try:
            user_account = UserAccount(
                debtor_name=debtor_name,
                debtor_phone_number=debtor_phone_number,
                amount=amount,
                user_id=user_id
            )
            db.session.add(user_account)
            db.session.commit()
            return jsonify(user_account.serialize()), 201
        except Exception as e:
            return jsonify({"Error": str(e)}), 401


@app.route("/delete-client", methods=['POST'])
def delete_account():
    if request.args:
        account_id = request.args.get('id')
        try:
            query = UserAccount.query.filter_by(id=account_id).one()
            if query:
                db.session.delete(query)
                db.session.commit()
                return jsonify({"message": "Account is deleted successfully"}), 200
            else:
                return jsonify({"message": "nothing found"}), 401
        except Exception as e:
            return jsonify({"Error": "this id is not exist"}), 401


@app.route("/get-client-account", methods=['GET'])
def get_user_account():
    if request.args:
        user_id = request.args.get('id')
        query = db.session.query(UserAccount).filter(UserAccount.user_id == user_id).all()
        if query:
            return jsonify({"message": "Success", "accounts": [e.serialize() for e in query]}), 200
        else:
            return jsonify({"message": "nothing found"}), 401


if __name__ == '__main__':
    app.run()
