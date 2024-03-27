from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import config
from app.model import db
from app.api.lookup import LookupResource

api = Api()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    api.add_resource(LookupResource, '/index')
    api.init_app(app)
    
    return app