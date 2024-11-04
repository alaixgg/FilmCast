from flask import request, jsonify
import jwt
import datetime
from functools import wraps

import logging
logging.basicConfig(level=logging.INFO)

from app import app

# Generate a JWT token
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # token expiration
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return token

# Decorator to verify token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Falta un token"}), 401
        try:
            # Ensure token format is "Bearer <token>"
            if "Bearer " in token:
                token = token.split(" ")[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido!"}), 401
        return f(*args, **kwargs)
    return decorated