from flask import Flask, jsonify
from app.database import db
from app.config import config_database, config_routes
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="/static")

def init_app(app=app):
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024 # 5 MB
    config_database(db)
    config_routes(app)
    CORS(app, supports_credentials=True)

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "error": "Imagem excede o tamanho máximo permitido (5MB)"
        }), 413

    return app