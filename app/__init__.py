from flask import Flask
from app.database import db
from app.config import config_database, config_routes
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="/static")

def init_app(app=app):
    # Aplicar CORS globalmente (desenvolvimento)
    config_database(db)
    config_routes(app)
    CORS(app)

    return app