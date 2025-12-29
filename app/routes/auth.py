from flask import Blueprint, jsonify, request, make_response
from app.middlewares.auth_middlewares import auth_required
from app.utils.jwt import generate_jwt
from app.utils.google_oauth import verify_google_token
from app.services.auth_services import login_with_google
from app.services.user_services import get_user_by_id
from app.config import JWT_EXPIRES_IN


auth_bp = Blueprint('auth', __name__)

@auth_bp.post("/google")
def google_login():
    google_info = verify_google_token(request.json["token"])
    user = login_with_google(google_info)

    token = generate_jwt(user)

    response = make_response(jsonify({
        "user": {
            "id": user.public_id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar
        }
    }))

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=False,    
        samesite="Lax",
        max_age=JWT_EXPIRES_IN,
        path="/"
    )

    return response

@auth_bp.get("/me")
@auth_required
def get_current_user():
    id = request.user["sub"]
    user = get_user_by_id(id)
    
    if not user:
        return jsonify({
            "error": True,
            "message": "Usuário não encontrado."
        }), 404
    
    return jsonify({
        "error": False,
        "message": "Usuário encontrado com sucesso!",
        "user": {
            "name": user.name,
            "email": user.email,
            "avatar": user.avatar,
            "public_id": user.public_id
        }
    })

@auth_bp.post("/logout")
def logout():   
    response = make_response({"message": "Terminou sessão."})
    response.delete_cookie("access_token")
    return response