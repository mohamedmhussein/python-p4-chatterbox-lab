from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ["GET", "POST"])
def messages():
    msg = Message.query.order_by(Message.created_at.asc()).all()
    
    if request.method == "GET":
        msg_dict = [message.to_dict() for message in msg]
        response = make_response(jsonify(msg_dict),200)
        return response
    elif request.method =="POST":
        msg = request.get_json()
        new_message = Message(body = msg["body"], username = msg["username"])
        db.session.add(new_message)
        db.session.commit()
        response = make_response()
        new_message_dict = new_message.to_dict()
        response = make_response(jsonify(new_message_dict), 201)
        return response

    

@app.route('/messages/<int:id>', methods = ["PATCH", "DELETE"])
def messages_by_id(id):
    msg = Message.query.filter(Message.id == id).first()

    if request.method == "DELETE":
        db.session.delete(msg)
        db.session.commit()
        response= make_response({
            "delete_successful": True,
            "message": "Review deleted."
        },200)
        return response
    elif request.method == "PATCH":
        updated_msg = request.get_json()
        for attr in updated_msg:
            setattr(msg, attr, updated_msg[attr])
            db.session.add(msg)
            db.session.commit()
            msg_dict = msg.to_dict()
            response = make_response(msg_dict,200)
            return response

if __name__ == '__main__':
    app.run(port=5555)
