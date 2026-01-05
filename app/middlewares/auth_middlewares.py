from flask import request, jsonify
from app.utils.jwt import decode_jwt
from app.services.user_services import get_user_by_id

def auth_required(fn):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")

        if request.method == "OPTIONS":
            return "", 200

        if not token:
            return jsonify({
                "error": True,
                "message": "Não autorizado! Faça login novamente."
            }), 401
        try:
            payload = decode_jwt(token)
            request.user = payload
            request.user_id = payload.get("sub")
        except Exception:
            return jsonify({
                "error": True,
                "message": "Não autorizado! Faça login novamente."
            }), 401
            
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def is_admin(fn):
    def wrapper(*args, **kwargs):
        user_id = request.user["sub"]
        user_data = get_user_by_id(user_id)

        if request.method == "OPTIONS":
            return "", 200

        if not user_data:
            return jsonify({
                "error": True,
                "message": "Não autorizado! Faça login novamente."
            }), 403

        user_role = user_data.role
        
        if user_role != "admin":
            return jsonify({
                "error": True,
                "message": "Acesso negado! Permissão insuficiente.",
                "status_code": 403
            }), 403
            
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper