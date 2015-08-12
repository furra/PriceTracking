from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.testing

@app.route('/')
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)