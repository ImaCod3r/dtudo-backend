from flask import Flask

app = Flask(__name__)

def init_app(app=app):
    from app.config import config_database
    config_database()


    return app