from flask import Flask
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from urllib.parse import quote_plus
from flask_marshmallow import Marshmallow

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "822572a49a49de3d68b7e21f8a39c61eb6178108a503a81c530554ad7af75167"
    password = quote_plus("qecoszslbouVAOUL")
    uri = f"mongodb+srv://manavparmar43:{password}@cluster0.i2ppjsv.mongodb.net/?retryWrites=true&w=majority"
    app.config["MONGODB_SETTINGS"] = {
        "host": f"mongodb+srv://manavparmar43:{password}@cluster0.i2ppjsv.mongodb.net/Banking?retryWrites=true&w=majority"
    }
    
    client = MongoClient(uri)
    try:
        client.admin.command("ping")
    except Exception as e:
        print(e)
    db = MongoEngine(app)
    ma = Marshmallow(app)
    
    return app,db,ma
