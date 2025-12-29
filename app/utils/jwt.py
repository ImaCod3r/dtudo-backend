import jwt
from datetime import datetime
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_IN

def _now_epoch():
    return int(datetime.utcnow().timestamp())

def generate_jwt(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "iat": _now_epoch(),
        "exp": _now_epoch() + int(JWT_EXPIRES_IN)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return token

def decode_jwt(token):
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not set. Set the JWT_SECRET env variable.")

    algorithms = [JWT_ALGORITHM] if isinstance(JWT_ALGORITHM, str) else JWT_ALGORITHM

    data = jwt.decode(
        token,
        JWT_SECRET,
        algorithms=algorithms
    )
    
    return data