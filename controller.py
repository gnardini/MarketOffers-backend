from flask import Flask, request
from flask_cors import CORS
import json
import socket
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client['market-offers']
usersDb = db['users']
offersDb = db['offers']

@app.route("/signup", methods=['POST'])
def signup():
    data = request.data
    data = json.loads(data)
    username = data['username']
    password = data['password']
    age = data['age']
    sex = data['sex']
    new_user = {
        'username': username,
        'password': password,
        'age': age,
        'sex': sex
    }
    user_exists = usersDb.find( { "username": username } ).count() > 0
    if user_exists:
        return "User already exists", 400
    else:
        user_id = usersDb.insert_one(new_user).inserted_id
        return json.JSONEncoder().encode(str(user_id))

@app.route("/login", methods=['POST'])
def login():
    data = request.data
    data = json.loads(data)
    username = data['username']
    password = data['password']
    user = usersDb.find_one( { "username": username, "password": password } )
    if user:
        user_id = str(user['_id'])
        return json.JSONEncoder().encode(user_id)
    else:
        return "Invalid user or password", 400

@app.route("/offer", methods=['POST'])
def create_offer():
    data = request.form
    description = data['description']
    aisle = data['aisle']
    sex = data['sex']
    min_age = data['min_age']
    max_age = data['max_age']
    new_offer = {
        'description': description,
        'aisle': aisle,
        'sex': sex,
        'min_age': int(min_age),
        'max_age': int(max_age)
    }
    offersDb.insert_one(new_offer)
    return "Created", 201

@app.route("/delete_offer", methods=['DELETE'])
def delete_offer():
    offer_id = request.form['id']
    offersDb.delete_one({'_id': ObjectId(offer_id)})
    return "deleted"

@app.route("/fetch_offers")
def request_offers():
    user_id = request.args.get('user_id')
    user = usersDb.find_one( { "_id": ObjectId(user_id) } )
    if not user:
        return "Invalid user id", 400
    aisles = {
        "8a21138990e1ebcd058f6b8485d13e31": 1,
        "35393280630e846f9e9dafd54785550b": 2,
        "8fc235de0ae8970001cc12102f6e3b0e": 3
    }
    offers = db.offers.find({
        "min_age": { "$lte": user['age'] },
        "max_age": { "$gte": user['age'] },
        # "sex": { "$in": ["A", user['sex']] }
    })
    return dumps(offers)

@app.route("/fetch_all_offers")
def open():
    offers = offersDb.find({})
    return dumps(offers)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print('IP: %s' % get_ip_address())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
