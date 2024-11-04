from flask import request, jsonify
import logging
logging.basicConfig(level=logging.INFO)

from app import app
from token_mod import token_required
from conn_mod import get_db_connection

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
def post_perfil():  # Changed from edit_pefil to edit_perfil
    data = request.get_json()
    id_usuario = request.user_id
    logging.info(f"Se va a editar el usuario {id_usuario}")

    telefono = data.get('telefono')
    email = data.get('email')
    descripcion = data.get('descripcion')
    pais = data.get('Pais')

    connection = None
    try:
        # Establish database connection
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Update user details by user ID
            cursor.execute("""
                UPDATE usuarios 
                SET telefono = %s, email = %s, descripcion = %s, Pais = %s 
                WHERE id = %s
            """, (telefono, email, descripcion, pais, id_usuario))
            connection.commit()
            
            logging.info("Se actualiza info en DB")
            return jsonify({"message": "Se actualiza info en DB"}), 201
    
    except Exception as e:
        logging.error(f"Error en la base de datos al editar el perfil: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()
