from flask import Flask, request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
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
    data = request.data
    data = json.loads(data)
    offer_id = data['id']
    description = data['description']
    # TODO: Save offer

@app.route("/fetch_offers")
def request_offers():
    user_id = request.args.get('user_id')
    user = usersDb.find_one( { "_id": ObjectId(user_id) } )
    if not user:
        return "Invalid user id", 400
    if user['sex'] == "MALE":
        offers = {
            "8a21138990e1ebcd058f6b8485d13e31": {
                "description": "2x1 Pringles",
                "id": 20
            },
            "35393280630e846f9e9dafd54785550b": {
                "description": "15% en Pepsi 2L",
                "id": 16
            },
            "8fc235de0ae8970001cc12102f6e3b0e": {
                "description": "50% Agua Sierra de los Padres 2L",
                "id": 10
            }
        }
    else:
        offers = {
            "8a21138990e1ebcd058f6b8485d13e31": {
                "description": "2x1 Papas Lays",
                "id": 21
            },
            "35393280630e846f9e9dafd54785550b": {
                "description": "10% en Cola Cola 2L",
                "id": 17
            },
            "8fc235de0ae8970001cc12102f6e3b0e": {
                "description": "50% Agua Villavicencio 5L",
                "id": 11
            }
        }
    return json.JSONEncoder().encode(offers)

@app.route("/fetch_all_offers")
def open():
    offers = offersDb.find({})
    # TODO: filter offers fields
    return json.JSONEncoder().encode(offers)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
