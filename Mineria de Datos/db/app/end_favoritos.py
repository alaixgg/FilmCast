from flask import request, jsonify
import logging

from app import app
from mod_token import token_required
from mod_conn import get_db_connection

logging.basicConfig(level=logging.INFO)

# obtener favoritos
@app.route('/mis_favoritos', methods=['GET'])
@token_required
def get_favoritos():
    id_usuario = request.user_id
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.name, a.gender, a.genre_specialization
                FROM favoritos f
                JOIN actores a ON f.actor_id = a.id
                WHERE f.usuario_id = %s
            """, (id_usuario,))
            favoritos = cursor.fetchall()
        
        if not favoritos:
            logging.warning(f"||get_favoritos|| No se encontraron favoritos para el usuario {id_usuario}.")
            return jsonify({"error": "No se encontraron favoritos asociados a este usuario."}), 404

        # Structure the actor data as a list of dictionaries
        column_names = [column[0] for column in cursor.description]  # Get column names from cursor
        favoritos_data = [
            dict(zip(column_names, favorito))  # Create a dictionary for each actor using column names
            for favorito in favoritos
        ]         
        
        logging.info(f"||get_favoritos|| {len(favoritos_data)} favoritos cargados para el usuario {id_usuario}.")
        return jsonify(favoritos_data), 200

    except Exception as e:
        logging.error(f"||get_favoritos|| Error al obtener favoritos para el usuario {id_usuario}: {e}")
        return jsonify({"error": "Problema en la base de datos."}), 500

    finally:
        if connection:
            connection.close()

# guardar favorito
@app.route('/guardar_favorito/<int:actor_id>', methods=['POST'])
@token_required
def post_favorito(actor_id):
    id_usuario = request.user_id
    connection = None

    try:
        # Establish a connection to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if the favorite already exists
            cursor.execute(
                'SELECT * FROM favoritos WHERE usuario_id = %s AND actor_id = %s',
                (id_usuario, actor_id)
            )
            existing_favorito = cursor.fetchone()
            
            if existing_favorito:
                logging.warning(f"||post_favorito|| El actor {actor_id} ya está en los favoritos del usuario {id_usuario}.")
                return jsonify({"message": "El actor ya está en sus favoritos."}), 409

            # Insert the favorite actor for the user
            cursor.execute(
                'INSERT INTO favoritos (usuario_id, actor_id) VALUES (%s, %s)',
                (id_usuario, actor_id)
            )
            connection.commit()

            logging.info(f"||post_favorito|| Favorito agregado para el usuario {id_usuario}: actor {actor_id}.")
            return jsonify({"message": "Favorito guardado exitosamente."}), 201

    except Exception as e:
        logging.error(f"||post_favorito|| Error al guardar favorito para el usuario {id_usuario}: {e}")
        return jsonify({"error": "Problema al guardar el favorito en la base de datos."}), 500

    finally:
        if connection:
            connection.close()
            
# eliminar favorito
@app.route('/eliminar_favorito/<int:actor_id>', methods=['POST'])
@token_required
def del_favorito(actor_id):
    id_usuario = request.user_id
    connection = None

    try:
        # Establish a connection to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Attempt to delete the favorite actor for the user
            cursor.execute(
                'DELETE FROM favoritos WHERE usuario_id = %s AND actor_id = %s',
                (id_usuario, actor_id)
            )
            affected_rows = cursor.rowcount  # Get the number of affected rows
            
            if affected_rows == 0:
                logging.warning(f"||del_favorito|| Intento de eliminar favorito fallido: actor {actor_id} no encontrado para usuario {id_usuario}.")
                return jsonify({"message": "No se encontró el favorito para eliminar."}), 404
            
            connection.commit()
            logging.info(f"||del_favorito|| Favorito eliminado para usuario {id_usuario}: actor {actor_id}.")
            return jsonify({"message": "Favorito eliminado exitosamente."}), 200

    except Exception as e:
        logging.error(f"||del_favorito|| Error al eliminar favorito para usuario {id_usuario}: {e}")
        return jsonify({"error": "Problema al eliminar el favorito en la base de datos."}), 500

    finally:
        if connection:
            connection.close()
