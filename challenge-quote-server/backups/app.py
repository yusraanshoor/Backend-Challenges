from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
import random

app = Flask(__name__)

f = open('quotes.json')
quotes = json.load(f)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Quote Server!  Ask for /quotes/random, or /quotes"


@app.route('/quotes', methods=['GET'])
def get_quotes():
    return jsonify(quotes)

@app.route('/quotes/random', methods = ['GET'])
def get_random_quote():
    return jsonify(pick_from_list(quotes))


def pick_from_list(list):
    return random.choice(list)