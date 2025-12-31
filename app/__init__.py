from flask import Flask, jsonify, request
from app.database import db
from app.config import config_database, config_routes
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="/static")

def init_app(app=app):
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB
    config_database(db)
    config_routes(app)

    # Allow the frontend origin during development. Use exact origin (no trailing slash).
    CORS(app,
         resources={r"/*": {"origins": "http://localhost:5173"}},
         supports_credentials=True)
    
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return '', 200

    @app.after_request
    def cors(response):
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "error": "Imagem excede o tamanho máximo permitido (5MB)"
        }), 413

    return app