from flask import Flask, jsonify
from pymongo import MongoClient
# from bson.json_util import dumps as json
import os

app = Flask(__name__)
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.price_tracking

@app.route('/')
def hello():
    return "hello world"

@app.route('/televisions', methods=['GET'])
def get_televisions():
  televisions = []
  for television in db.televisions.find():
    television.pop('_id')
    televisions.append(television)
  return jsonify({'televisions':televisions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)