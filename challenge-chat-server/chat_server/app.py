from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://yusraanshoor@localhost/chat_server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key = True)
    sent_from = db.Column(db.String(), nullable = False)
    text = db.Column(db.String(), nullable = False)
    time_sent = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __repr__(self):
        return '<Message %r>' % self.text #what are you meant to choose for this???

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Chat Server API!"

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        return get_messages()
    elif request.method == 'POST':
        return add_message(request.json)

def get_messages():
    messages = db.session.query(Message).all()
    listed_messages = [format_message_as_dict(message) for message in messages]
    return jsonify(listed_messages)

def add_message(data):
    message = Message(sent_from = data["sent_from"], text = data["text"])
    db.session.add(message)
    db.session.commit()
    return "Message Added!", 200


@app.route('/messages/<id>', methods= ['GET', 'DELETE'])
def message_id(id):
    if request.method == 'GET':
        return get_message_by_id(id)
    if request.method == 'DELETE':
        return delete_message_by_id(id)


def get_message_by_id(id):
    message = db.session.query(Message).filter(Message.id == id).first()
    return jsonify(format_message_as_dict(message))

def delete_message_by_id(id):
    message = db.session.query(Message).filter(Message.id == id).first()
    db.session.delete(message)
    db.session.commit()
    return "Message Deleted!", 200


def format_message_as_dict (message):
    return {
        "id": message.id, "sent_from": message.sent_from, "text": message.text, "time_sent": message.time_sent
    }

