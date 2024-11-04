from flask import request, jsonify
import logging

from app import app
from mod_token import token_required
from mod_conn import get_db_connection

logging.basicConfig(level=logging.INFO)

# obtener perfil
@app.route('/perfil', methods=['GET'])
@token_required
def get_perfil():
    connection = None
    try:
        # Establish a connection to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, email, telefono, descripcion, Pais 
                FROM usuarios 
                WHERE id = %s
            """, (request.user_id,))
            user = cursor.fetchone()
        
        if user:
            # Create a dictionary with user data
            user_data = {
                "id": user[0],
                "email": user[1],
                "telefono": user[2],
                "descripcion": user[3],
                "nacionalidad": user[4]
            }
            logging.info(f"||get_perfil|| Información de usuario {user[0]} enviada exitosamente.")
            return jsonify(user_data), 200
        else:
            logging.warning(f"||get_perfil|| Usuario con ID {request.user_id} no encontrado.")
            return jsonify({"error": "Usuario no encontrado"}), 404
    
    except Exception as e:
        logging.error(f"||get_perfil|| Error en la base de datos al obtener el perfil del usuario {request.user_id}: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()
            logging.info("Conexión a la base de datos cerrada.")

# editar perfil
@app.route('/editar_perfil', methods=['POST'])
@token_required
def post_perfil():
    data = request.get_json()
    id_usuario = request.user_id

    telefono = data.get('telefono')
    email = data.get('email')
    descripcion = data.get('descripcion')
    pais = data.get('Pais')

    # Validate input data
    if not all([telefono, email, descripcion, pais]):
        logging.warning("||post_perfil|| Faltan datos necesarios para actualizar el perfil.")
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    connection = None
    try:
        # Establish a connection to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Update user details in the database
            cursor.execute("""
                UPDATE usuarios 
                SET telefono = %s, email = %s, descripcion = %s, Pais = %s 
                WHERE id = %s
            """, (telefono, email, descripcion, pais, id_usuario))
            connection.commit()

            if cursor.rowcount == 0:
                logging.warning(f"||post_perfil|| No se encontraron cambios para el usuario {id_usuario}.")
                return jsonify({"message": "No se realizaron cambios."}), 204

            logging.info(f"||post_perfil|| Información del usuario {id_usuario} actualizada en la base de datos.")
            return jsonify({"message": "Perfil actualizado exitosamente."}), 200
    
    except Exception as e:
        logging.error(f"||post_perfil|| Error en la base de datos al editar el perfil del usuario {id_usuario}: {e}")
        return jsonify({"error": "Problema en la base de datos."}), 500
    
    finally:
        if connection:
            connection.close()
            logging.info("Conexión a la base de datos cerrada.")
