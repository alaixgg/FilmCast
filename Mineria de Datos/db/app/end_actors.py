from flask import request, jsonify
import logging
from app import app
from mod_token import token_required
from mod_conn import get_db_connection

logging.basicConfig(level=logging.INFO)

# info_actor
@app.route('/info_actor/<int:actor_id>', methods=['GET'])
@token_required
def get_actor(actor_id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM actores WHERE id = %s", (actor_id,))
            actor_info = cursor.fetchone()

            if actor_info:
                column_names = [desc[0] for desc in cursor.description]
                actor_data = dict(zip(column_names, actor_info))
                logging.info(f"||get_actor|| Se envía información del actor {actor_id}.")
                return jsonify(actor_data), 200
                
            else:
                logging.warning(f"||get_actor|| No se encontró el actor con ID {actor_id}.")
                return jsonify({"error": "No se encuentra actor"}), 404
    
    except Exception as e:
        logging.error(f"||get_actor|| Error en la base de datos al cargar el actor con ID {actor_id}: {e}")
        return jsonify({"error": "Problema en la base de datos."}), 500
    
    finally:
        if connection:
            connection.close()

# enviar 4 actores random
@app.route('/destacados', methods=['GET'])
@token_required
def get_destacados():
    connection = None
    try:
        connection = get_db_connection()        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM actores ORDER BY RAND() LIMIT 4")
            actors = cursor.fetchall()

            if not actors:
                logging.warning("||get_destacados|| No se encontraron actores destacados en la base de datos.")
                return jsonify({"error": "No se encontraron actores destacados"}), 404

            column_names = [column[0] for column in cursor.description]
            actors_data = [
                dict(zip(column_names, actor))  # Create a dictionary for each actor using column names
                for actor in actors
            ]

            logging.info(f"||get_destacados|| Se envía información de {len(actors_data)} actores destacados.")
            return jsonify(actors_data), 200

    except Exception as e:
        logging.error(f"||get_destacados|| Error al obtener actores destacados: {e}")
        return jsonify({"error": "Problema al obtener actores destacados"}), 500

    finally:
        if connection:
            connection.close()
