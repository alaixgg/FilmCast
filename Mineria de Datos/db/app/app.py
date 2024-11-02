#!/usr/bin/env python
"""
Casting Inteligente: Algoritmos para la selección óptima de actores

Copyright (C) 2024  Alvarado Ludwig

Este archivo es parte de FilmCast.

FilmCast es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal como fue publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia o cualquier versión posterior.

FilmCast se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con FilmCast. Si no, consulta https://www.gnu.org/licenses/.
"""

import os
from flask import Flask, request, jsonify
import jwt
import bcrypt
import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql.cursors
from redis import Redis
import time

import logging

logging.basicConfig(level=logging.INFO)




app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Use a fallback key if SECRET_KEY is not set

redis_client = Redis(host='redis', port=6379)

# You can also use other environment variables for DB connection, if needed:
host_env = os.getenv('DB_HOST')
user_env = os.getenv('DB_USER')
pass_env = os.getenv('DB_PASSWORD')
db_env = os.getenv('DB_NAME')

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379"  # Use service name as host
)
limiter.init_app(app)   

# Helper to connect to the DB
def get_db_connection(host=None, user=None, password=None, database=None):
    while True:
        try:
            connection = pymysql.connect(
                host=host_env,
                user=user_env,
                password=pass_env,
                database=db_env
            )
            return connection
        except pymysql.err.OperationalError as e:
            logging.warning(f"Error!!!!! -> {e}")
            logging.warning("Database connection failed, retrying in 5 seconds...")
            time.sleep(5)


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
            return jsonify({"error": "Token is missing!"}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = payload['user_id']  # Attach user_id to request for access control
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated

# Register endpoint
@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input data
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400
    
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO users (username, password_hash) VALUES ({username}, {hashed_password})")
            connection.commit()
    except Exception as e:
        logging.error("Database error during registration: %s", e)
        return jsonify({"error": "Database error"}), 500
    finally:
        connection.close()
    
    return jsonify({"message": "Usuario registrado!"}), 201


# Login endpoint
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit to prevent abuse
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password, user['password_hash'].encode('utf-8')):
        token = generate_token(user_id=user['id'])
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Protected data endpoint
@app.route('/data', methods=['GET'])
@token_required
def get_data():
    # Only accessible by logged-in users with valid tokens
    return jsonify({"data": "Here is your protected data!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
