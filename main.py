from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/signup", methods=['POST'])
def signup():
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
            return jsonify(user.serialize()), 200
        except Exception as e:
            return jsonify({'Error': e}), 401
    else:
        return jsonify({'Error': 'please input correct data'}), 401


@app.route("/get-users")
def get_all():
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users]), 200
    except Exception as e:
        return str(e), 401


if __name__ == '__main__':
    app.run()
