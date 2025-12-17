from flask import Blueprint, jsonify, request
from app.services.auth_services import login_with_google
from app.utils.google_oauth import verify_google_token
from app.utils.jwt import generate_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/google')
def google_login():
    google_info = verify_google_token(request.json["token"])
    user = login_with_google(google_info)
    token = generate_jwt(user)

    return jsonify({
        "error": False,
        "message": "Login efectuado com sucesso!",
        "user": {
            "public_id": user.public_id,
            "name": user.name,
            "email": user.email,
            "avatar": user.avatar
        },
        "token": token
    }), 200