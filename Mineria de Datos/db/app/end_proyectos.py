from flask import request, jsonify
import logging
import datetime

from app import app
from mod_token import token_required
from mod_conn import get_db_connection

logging.basicConfig(level=logging.INFO)

# obtener mis proyectos
@app.route('/mis_proyectos', methods=['GET'])
@token_required
def get_proyectos():
    id_usuario = request.user_id
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.titulo, p.descripcion, p.genero, p.fecha_inicio, p.fecha_fin, p.presupuesto 
                FROM proyectos p
                JOIN actividad a ON p.id = a.proyecto_id
                WHERE a.usuario_id = %s
            """, (id_usuario,))
            proyectos = cursor.fetchall()
        
        if not proyectos:
            logging.warning(f"||get_proyectos|| No se encontraron proyectos para el usuario {id_usuario}.")
            return jsonify({"error": "No se encontraron proyectos asociados a este usuario."}), 404

        column_names = [column[0] for column in cursor.description]  # Get column names from cursor
        proyectos_data = [
            dict(zip(column_names, proyecto))  # Create a dictionary for each project using column names
            for proyecto in proyectos
        ]
        
        logging.info(f"||get_proyectos|| Se envía información de {len(proyectos_data)} proyectos para el usuario {id_usuario}.")
        return jsonify(proyectos_data), 200
    
    except Exception as e:
        logging.error(f"||get_proyectos|| Error en la base de datos al obtener los proyectos para el usuario {id_usuario}: {e}")
        return jsonify({"error": "Problema en la base de datos."}), 500
    
    finally:
        if connection:
            connection.close()
            
# obtener info de proyecto
@app.route('/info_proyecto/<int:proyecto_id>', methods=['GET'])
@token_required
def get_proyecto(proyecto_id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch the project information by ID
            cursor.execute("SELECT * FROM proyectos WHERE id = %s", (proyecto_id,))
            proyecto_info = cursor.fetchone()

        if not proyecto_info:
            logging.warning(f"||get_proyecto|| No se encontró el proyecto con ID {proyecto_id} en la base de datos.")
            return jsonify({"error": "No se encontró proyecto."}), 404

        # Retrieve column names and create a dictionary for the project
        column_names = [column[0] for column in cursor.description]  # Get column names from cursor
        proyecto_data = dict(zip(column_names, proyecto_info))  # Create a dictionary for the project using column names

        logging.info(f"||get_proyecto|| Se envía información del proyecto {proyecto_id}")
        return jsonify(proyecto_data), 200

    except Exception as e:
        logging.error(f"||get_proyecto|| Error en la base de datos al obtener el proyecto con ID {proyecto_id}: {e}")
        return jsonify({"error": "Problema en la base de datos."}), 500

    finally:
        if connection:
            connection.close()
            
# crear proyecto
@app.route('/crear_proyecto', methods=['POST'])
@token_required
def post_proyecto():
    data = request.get_json()
    id_usuario = request.user_id
    connection = None

    # Extracting data from request
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    genero = data.get('genero')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    presupuesto = data.get('presupuesto')
    actores_seleccionados = data.get('actores_seleccionados', [])

    logging.info(f"||post_proyecto|| Attempting to insert project with values: "
                  f"{titulo}, {descripcion}, {genero}, {fecha_inicio}, {fecha_fin}, {presupuesto}")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check for existing project
            cursor.execute("""
                SELECT COUNT(*) FROM proyectos 
                WHERE titulo = %s AND descripcion = %s AND genero = %s 
                AND fecha_inicio = %s AND fecha_fin = %s AND presupuesto = %s
            """, (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto))
            count = cursor.fetchone()[0]

            logging.debug(f"||post_proyecto|| Count of existing projects: {count}")
            if count > 0:
                logging.warning(f"||post_proyecto|| Proyecto ya existe para el usuario {id_usuario}.")
                return jsonify({"error": "Ya existe un proyecto exactamente igual. Por favor, modifica los detalles."}), 409

            # Insert new project
            cursor.execute("""
                INSERT INTO proyectos (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto))
            
            proyecto_id = cursor.fetchone()[0]
            logging.info(f"||post_proyecto|| Proyecto guardado con ID {proyecto_id}.")

            # Insert associated actors
            for actor in actores_seleccionados:
                logging.debug(f"||post_proyecto|| Inserting actor with ID {actor} for project {proyecto_id}.")
                cursor.execute("""
                    INSERT INTO actividad (usuario_id, proyecto_id, actor_id, rol, fecha_inicio)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_usuario, proyecto_id, actor, None, datetime.datetime.now()))

            connection.commit()
            logging.info(f"||post_proyecto|| Proyecto agregado para el usuario {id_usuario} con ID de proyecto {proyecto_id}.")
            return jsonify({"message": "Proyecto guardado exitosamente."}), 201

    except Exception as e:
        logging.error(f"||post_proyecto|| Error al guardar proyecto para el usuario {id_usuario}: {e}")
        return jsonify({"error": "Problema al guardar el proyecto en la base de datos."}), 500

    finally:
        if connection:
            connection.close()
            logging.info(f"||post_proyecto|| Closed database connection.")
            
# eliminar proyecto
@app.route('/eliminar_proyecto/<int:proyecto_id>', methods=['POST'])
@token_required
def del_proyecto(proyecto_id):
    id_usuario = request.user_id
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Delete activities associated with the project
            cursor.execute('DELETE FROM actividad WHERE proyecto_id = %s', (proyecto_id,))
            affected_rows = cursor.rowcount  # Get the number of affected rows
            connection.commit()

            if affected_rows > 0:
                logging.info(f"||del_proyecto|| Proyecto {proyecto_id} eliminado para el usuario {id_usuario}.")
                return jsonify({"message": "Proyecto eliminado exitosamente."}), 200
            else:
                logging.warning(f"||del_proyecto|| Intento de eliminar proyecto {proyecto_id} no tuvo éxito; no se encontraron actividades relacionadas.")
                return jsonify({"message": "No se encontraron actividades relacionadas para eliminar."}), 404

    except Exception as e:
        logging.error(f"||del_proyecto|| Error al eliminar el proyecto {proyecto_id} para el usuario {id_usuario}: {e}")
        return jsonify({"error": "Error al eliminar el proyecto en la base de datos."}), 500

    finally:
        if connection:
            connection.close()
