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

# Register endpoint
@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input data
    usuario = data.get('nombre')
    contrasena = data.get('clave')
    descripcion = data.get('descripcion')
    pais = data.get('Pais')
    telefono = data.get('telefono')
    correo = data.get('email')
    
    if not usuario or not contrasena:
        return jsonify({"error": "Se requiere usuario y contraseña!"}), 400
    
    password = contrasena.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if the user already exists
            cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (usuario,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return jsonify({"error": "Usuario ya existe!"}), 409
            
            # Insert new user if no existing user found
            cursor.execute("INSERT INTO usuarios (nombre, clave, descripcion, Pais, telefono, email) VALUES (%s, %s, %s, %s, %s, %s)",
            (usuario, hashed_password, descripcion, pais, telefono, correo))
            connection.commit()
    except Exception as e:
        logging.error(f"Error en bdd durante el registro: {e}")
        return jsonify({"error": "Problema en la bdd"}), 500
    finally:
        connection.close()
    
    return jsonify({"message": "Usuario registrado!"}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting to prevent abuse
def login():
    data = request.get_json()
    usuario = data.get('nombre')
    contrasena = data.get('clave')
    
    if not usuario or not contrasena:
        logging.error(f"Error: Se requiere nombre de usuario y contraseña!")
        return jsonify({"error": "Se requiere nombre de usuario y contraseña!"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, clave FROM usuarios WHERE nombre = %s", (usuario,))
            user = cursor.fetchone()
        
        if user and bcrypt.checkpw(contrasena.encode('utf-8'), user[1].encode('utf-8')):
            token = generate_token(user_id=user[0])
            logging.info(f"Ha entrado el usuario {usuario}")
            return jsonify({"token": token}), 200
        else:
            logging.error(f"Error: Credenciales inválidas para usuario {usuario}")
            return jsonify({"error": "Credenciales inválidas"}), 401
    
    except Exception as e:
        logging.error(f"Error en la base de datos durante el inicio de sesión: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()

# Protected data endpoint
@app.route('/data', methods=['GET'])
@token_required
def get_data():
    # Only accessible by logged-in users with valid tokens
    return jsonify({"data": "Here is your protected data!"}), 200

# obtener perfil
@app.route('/perfil', methods=['GET'])
@token_required
def get_perfil():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, email, telefono, descripcion, Pais 
                FROM usuarios 
                WHERE id = %s
            """, (request.user_id,))
            user = cursor.fetchone()
        
        if user:
            user_data = {
                "id": user[0],
                "email": user[1],
                "telefono": user[2],
                "descripcion": user[3],
                "nacionalidad": user[4]
            }
            logging.info(f"Se envía información de usuario {user[0]}")
            return jsonify(user_data), 200
        else:
            logging.error("Error: Usuario no encontrado")
            return jsonify({"error": "Usuario no encontrado"}), 404
    
    except Exception as e:
        logging.error(f"Error en la base de datos al obtener el perfil: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()

# editar perfil
@app.route('/editar_perfil', methods=['POST'])
@token_required
def edit_pefil():
    data = request.get_json()
    id_usuario=request.user_id
    logging.info(f"Se va a editar el usuario {id_usuario}")

    telefono = data.get('telefono')
    email = data.get('email')
    descripcion = data.get('descripcion')
    Pais = data.get('Pais')

    connection = None
    try:
        # Establish database connection
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch user details by user ID
            cursor.execute("""
                UPDATE usuarios 
                SET telefono = %s, email = %s, descripcion = %s, Pais = %s 
                WHERE id = %s
            """, (telefono, email, descripcion, Pais, id_usuario, ))
            connection.commit()
            connection.close()
            
            logging.info(f"Se actualiza info en DB")
            jsonify({"message": "Se actualiza info en DB"}), 201
    
    except Exception as e:
        logging.error(f"Error en la base de datos al obtener el perfil: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
