from flask import request, jsonify
import bcrypt
import logging
logging.basicConfig(level=logging.INFO)

from conn_mod import get_db_connection
from token_mod import generate_token
from app import app, limiter

# Register endpoint
@app.route('/registro', methods=['POST'])
def post_register():
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
def post_login():
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
