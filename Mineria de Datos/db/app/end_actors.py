from flask import request, jsonify
import logging
logging.basicConfig(level=logging.INFO)

from app import app
from token_mod import token_required
from conn_mod import get_db_connection

# info_actor
@app.route('/info_actor/<int:actor_id>', methods=['GET'])
@token_required
def get_actor(actor_id):

    connection = None
    try:
        # Establish database connection
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Update user details by user ID
            cursor.execute("SELECT * FROM actores WHERE id = %s", (actor_id,))
            actor_info = cursor.fetchone()

            if actor_info:
                column_names = [desc[0] for desc in cursor.description]
                # Create dictionary by zipping column names and data
                user_data = dict(zip(column_names, actor_info))

            logging.info(f"Se envía información de actor {actor_id}")
            return jsonify(user_data), 200
    
    except Exception as e:
        logging.error(f"Error en la base de datos al cargar el actor: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()

# enviar 4 actores random
@app.route('/destacados', methods=['GET'])
@token_required
def get_destacados():
    connection = None
    try:
        # Establish database connection
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch 4 random actors
            cursor.execute("SELECT id, nombre, edad, biografia FROM actores ORDER BY RANDOM() LIMIT 4")
            actors = cursor.fetchall()
            
            if actors:
                # Structure the actor data as a list of dictionaries
                actors_data = [
                    {
                        "id": actor[0],
                        "nombre": actor[1],
                        "edad": actor[2],
                        "biografia": actor[3]
                    }
                    for actor in actors
                ]
                
                logging.info("Se envía información de 4 actores destacados")
                return jsonify(actors_data), 200
            else:
                logging.error("No se encontraron actores")
                return jsonify({"error": "No se encontraron actores"}), 404
    
    except Exception as e:
        logging.error(f"Error en la base de datos al obtener actores destacados: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()
