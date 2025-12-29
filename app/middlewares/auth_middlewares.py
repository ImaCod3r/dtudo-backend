from flask import request, jsonify
from app.utils.jwt import decode_jwt

def auth_required(fn):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")

        if request.method == "OPTIONS":
            return "", 200

        if not token:
            print("Sem token")
            return jsonify({
                "error": True,
                "message": "Não autorizado! Faça login novamente."
            }), 401
        try:
            payload = decode_jwt(token)
            request.user = payload
            request.user_id = payload.get("sub")
        except Exception:
            print("Decode misarevel")
            return jsonify({
                "error": True,
                "message": "Não autorizado! Faça login novamente."
            }), 401
            
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper