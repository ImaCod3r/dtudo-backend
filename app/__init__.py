from flask import Flask, jsonify, request
from app.database import db
from app.config import config_database, config_routes
from app.middlewares.log_middlewares import log_request
from flask_cors import CORS
from playhouse.pool import MaxConnectionsExceeded
import os


app = Flask(__name__, static_folder="static", static_url_path="/static")

def init_app(app=app):
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
    config_database(db)
    config_routes(app)

    # CORS configuration
    allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")]
    
    CORS(app,
         resources={r"/*": {
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"]
         }},
         supports_credentials=True)

    @app.before_request
    def before_request():
        if db.is_closed():
            try:
                db.connect(reuse_if_open=True)
            except MaxConnectionsExceeded:
                return jsonify({
                    "error": True,
                    "message": "Serviço temporariamente indisponível. Tente novamente em instantes."
                }), 503

    @app.get("/")
    def index():
        return jsonify({
            "message": "Bem-vindo ao DTudo!"
        }), 200
    
    @app.after_request
    def after_request_func(response):
        log_request(response)
        return response


    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "error": "Imagem excede o tamanho máximo permitido (5MB)"
        }), 413

    @app.errorhandler(MaxConnectionsExceeded)
    def handle_max_connections_exceeded(error):
        return jsonify({
            "error": True,
            "message": "Serviço temporariamente indisponível. Tente novamente em instantes."
        }), 503

    return app
