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
        print(content)
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


if __name__ == '__main__':
    app.run()
