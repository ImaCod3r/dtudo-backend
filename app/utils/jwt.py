import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_IN

def generate_jwt(user):
    payload = {
        "sub": user.id,
        "email": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRES_IN)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token

def decode_jwt(token):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=JWT_ALGORITHM
    )