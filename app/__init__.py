from flask import Flask
from app.database import db
from app.models.user import User

app = Flask(__name__)

def init_app():
    db.connect()
    db.create_tables([User]) 

    return app