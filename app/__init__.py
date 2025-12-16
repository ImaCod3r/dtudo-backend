from flask import Flask
from app.database import db
from app.config import config_database, config_routes

app = Flask(__name__)

def init_app(app=app):
    config_database(db)
    config_routes(app)

    return app