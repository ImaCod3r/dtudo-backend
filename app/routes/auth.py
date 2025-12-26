from flask import Blueprint, jsonify, request, make_response
from app.utils.jwt import generate_jwt
from app.utils.google_oauth import verify_google_token
from app.services.auth_services import login_with_google

auth_bp = Blueprint('auth', __name__)

@auth_bp.post("/google")
def google_login():
    google_info = verify_google_token(request.json["token"])
    user = login_with_google(google_info)

    token = generate_jwt(user)

    response = make_response(jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar
        }
    }))

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=False,     # True em produção (HTTPS)
        samesite="Lax",
        max_age=60 * 60 * 24
    )

    return response

@auth_bp.post("/logout")
def logout():   
    response = make_response({"message": "Terminou sessão."})
    response.delete_cookie("access_token")
    return response