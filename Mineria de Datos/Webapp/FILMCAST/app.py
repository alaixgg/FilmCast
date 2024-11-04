from flask import Flask, session, jsonify , redirect, url_for, render_template, request, flash
import pandas as pd 
import numpy as np
from openpyxl import Workbook
import os 
from datetime import datetime
import requests 
import random


app = Flask(__name__)
app.secret_key = 'tu_clave_secreta' 

import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123",
        database="1"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('contrasena')

        payload = {
            "nombre": usuario,
            "clave": clave
        }

        try:
            # Realizar la solicitud POST a la API de login
            response = requests.post('https://db.cuspide.club/login', json=payload)
            response.raise_for_status()
            resultado = response.json()

            # Imprimir respuesta para depuración
            print("Respuesta del servidor:", resultado)

            # Verificar si se recibió el token
            token = resultado.get('token')
            print("Token recibido:", token)  

            if token:
                # Guardar el token y otros datos del usuario en la sesión
                session['token'] = token
                session['id'] = resultado.get('id')
                session['usuario'] = resultado.get('nombre')
                session['email'] = resultado.get('email')
                session['telefono'] = resultado.get('telefono')
                session['descripcion'] = resultado.get('descripcion')
                session['nacionalidad'] = resultado.get('Pais')

                # Confirmar que el token fue guardado en la sesión
                print("Token guardado en la sesión:", session.get('token'))

                return redirect(url_for('menu'))
            else:
                # Si no se recibió un token, mostrar el error
                error = resultado.get('error', "No se recibió un token de autenticación.")
                print("Error en autenticación:", error)
                return render_template('login.html', error=error)

        except requests.exceptions.HTTPError as err:
            error = f"Error en la autenticación: {err.response.text}"
            print("HTTPError:", error)
            return render_template('login.html', error=error)

        except Exception as e:
            error = f"Ocurrió un error: {str(e)}"
            print("Exception:", error)
            return render_template('login.html', error=error)

    return render_template('login.html')



import requests
    
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario') 
        contrasena = request.form.get('contrasena')  
        confirmar_contrasena = request.form.get('confirmar_contrasena')

        if contrasena != confirmar_contrasena:
            error = "Las contraseñas no coinciden."
            return render_template('registro.html', error=error)
        
        payload = {
            "nombre": usuario,
            "clave": contrasena,
            "descripcion": '',
            "Pais": '',
            "telefono": '',
            "email": ''
        }

        try:
            response = requests.post('https://db.cuspide.club/registro', json=payload)
            response.raise_for_status()

            return redirect(url_for('login'))

        except requests.exceptions.HTTPError as err:
            error = f"Error al registrar usuario: {err}"
            return render_template('registro.html', error=error)
        except Exception as e:
            error = f"Ocurrió un error: {str(e)}"
            return render_template('registro.html', error=error)

    return render_template('registro.html')

@app.route('/perfil', methods=['GET'])
def perfil():
    if 'token' in session:
        token = session.get('token')
        headers = {
            'Authorization': f'Bearer {token}'
        }

        print("Token utilizado en la solicitud:", token)
        print("Encabezados enviados:", headers)

        try:
            response = requests.get('https://db.cuspide.club/perfil', headers=headers)
            response.raise_for_status()

            usuario_info = response.json()
            print("Información del usuario:", usuario_info)

            id = usuario_info.get('id', '')
            email = usuario_info.get('email', '')
            telefono = usuario_info.get('telefono', '')
            descripcion = usuario_info.get('descripcion', '')
            nacionalidad = usuario_info.get('nacionalidad', '')  # Asegúrate de que la clave sea correcta.

            session['id'] = id
            session['email'] = email
            session['telefono'] = telefono
            session['descripcion'] = descripcion
            session['nacionalidad'] = nacionalidad
            
            return render_template('perfil.html',
                                   id=id,
                                   email=email,
                                   telefono=telefono,
                                   descripcion=descripcion,
                                   nacionalidad=nacionalidad)

        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener información del usuario: {err.response.text}")
            session.pop('token', None)  
            return redirect(url_for('login'))
        except requests.exceptions.RequestException as e:
            print(f"Ocurrió un error de red: {str(e)}")
            return render_template('perfil.html', error="Ocurrió un error al conectar con la API.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {str(e)}")
            return render_template('perfil.html', error="Ocurrió un error al obtener información del usuario.")

    return redirect(url_for('login'))


@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario' in session:
        token = session.get('token')  

        if request.method == 'POST':
            nuevo_telefono = request.form.get('telefono')
            nuevo_email = request.form.get('email')
            nueva_descripcion = request.form.get('descripcion')
            nuevo_Pais = request.form.get('Pais')
            
            
            payload = {
                'telefono': nuevo_telefono,
                'email': nuevo_email,
                'descripcion': nueva_descripcion,
                'Pais': nuevo_Pais
            }
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            try:
                response = requests.put('https://db.cuspide.club/editar_perfil', json=payload, headers=headers)
                response.raise_for_status()  

                session['telefono'] = nuevo_telefono
                session['email'] = nuevo_email
                session['descripcion'] = nueva_descripcion
                session['nacionalidad'] = nuevo_Pais

                return redirect(url_for('perfil'))

            except requests.exceptions.HTTPError as err:
                print(f"Error al actualizar información del usuario: {err.response.text}")
                return render_template('editar_perfil.html', error="No se pudo actualizar el perfil.")
            except Exception as e:
                print(f"Ocurrió un error: {str(e)}")
                return render_template('editar_perfil.html', error="Ocurrió un error al actualizar el perfil.")

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get('https://db.cuspide.club/perfil', headers=headers)
            response.raise_for_status()
            usuario_data = response.json()

            return render_template('editar_perfil.html', 
                                   telefono=usuario_data.get('telefono', ''),
                                   email=usuario_data.get('email', ''),
                                   descripcion=usuario_data.get('descripcion', ''),
                                   Pais=usuario_data.get('Pais', ''))

        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener información del usuario: {err.response.text}")
            return render_template('editar_perfil.html', error="No se pudo obtener la información del perfil.")
        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")
            return render_template('editar_perfil.html', error="Ocurrió un error al obtener la información del perfil.")

    return redirect(url_for('login'))

@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    categorias = ["Age", "Years Active", "Beauty", "Skill Level", "Award Wins", "Media Mentions", "Social Media Followers", "Social Media Likes", "Network Size", "Income"]
    categorias_con_indices = list(enumerate(categorias))
    return render_template('busqueda.html')

@app.route('/consulta_actor_filtro', methods=['POST'])
def consulta_actor_filtro():
    try:
        vector_input_ranges = []
        for i in range(10):
            range_value = request.form.get(f'range_{i}')
            min_val, max_val = map(int, range_value.split('-'))
            vector_input_ranges.append([min_val, max_val])

        weights = [
            int(request.form[f'weight_{i}'])
            for i in range(10)
        ]

        api_url = 'https://model.cuspide.club/nearest-records'
        payload = {
            "ranges": vector_input_ranges,
            "weights": weights
        }

        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            actores = data.get('nearest_records', [])
            print(actores)  
            return render_template('actores_sin_filtro.html', nearest_records=actores)
        else:
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return render_template('actores_sin_filtro.html', nearest_records=[])

    except Exception as e:
        print(f"Error: {str(e)}")
        # Aquí es donde debes colocar el render en caso de excepción
        return render_template('actores_sin_filtro.html', nearest_records=[])


@app.route('/busqueda_filtro')
def busqueda_filtro():
    categorias_numericas = ["Age", "Years Active", "Beauty", "Skill Level", "Award Wins", "Media Mentions", "Social Media Followers", "Social Media Likes", "Network Size", "Income"]
    categorias_categoricas = ["Gender_Female", "Gender_Male", "Nationality_Canada", "Nationality_USA",
                              "Genre Specialization_Action", "Genre Specialization_Comedy",
                              "Genre Specialization_Drama", "Genre Specialization_Horror",
                              "Genre Specialization_Musical", "Genre Specialization_Sci-Fi",
                              "Education Level_College", "Education Level_Graduate",
                              "Education Level_High School", "Education Level_University"]
    
    categorias_numericas_con_indices = list(enumerate(categorias_numericas))
    categorias_categoricas_con_indices = list(enumerate(categorias_categoricas))
    
    return render_template('busqueda_filtro.html', 
                           categorias_numericas_con_indices=categorias_numericas_con_indices,
                           categorias_categoricas_con_indices=categorias_categoricas_con_indices)

@app.route('/consulta_actor', methods=['POST'])
def consulta_actor():
    try:
        vector_input_ranges = []
        for i in range(10):  # Se asume que hay 10 variables numéricas
            range_value = request.form.get(f'range_{i}')
            min_val, max_val = map(int, range_value.split('-'))
            vector_input_ranges.append((min_val, max_val))

        # Procesar las variables categóricas
        cat_variables = {
            "Gender_Female": int(request.form.get('gender_female', 0)),  # Devuelve 0 si no está marcada
            "Gender_Male": int(request.form.get('gender_male', 0)),      # Devuelve 0 si no está marcada
            "Nationality_Canada": int(request.form.get('nationality_canada', 0)), # Devuelve 0 si no está marcada
            "Nationality_USA": int(request.form.get('nationality_usa', 0)), # Devuelve 0 si no está marcada
            "Genre Specialization_Action": int(request.form.get('genre_action', 0)), # Devuelve 0 si no está marcada
            "Genre Specialization_Comedy": int(request.form.get('genre_comedy', 0)), # Devuelve 0 si no está marcada
            "Genre Specialization_Drama": int(request.form.get('genre_drama', 0)), # Devuelve 0 si no está marcada
            "Genre Specialization_Horror": int(request.form.get('genre_horror', 0)), # Devuelve 0 si no está marcada
            "Genre Specialization_Musical": int(request.form.get('genre_musical', 0)), # Devuelve 0 si no está marcada
            "Genre Specialization_Sci-Fi": int(request.form.get('genre_sci_fi', 0)), # Devuelve 0 si no está marcada
            "Education Level_College": int(request.form.get('education_college', 0)), # Devuelve 0 si no está marcada
            "Education Level_Graduate": int(request.form.get('education_graduate', 0)), # Devuelve 0 si no está marcada
            "Education Level_High School": int(request.form.get('education_high_school', 0)), # Devuelve 0 si no está marcada
            "Education Level_University": int(request.form.get('education_university', 0)) # Devuelve 0 si no está marcada
        }

        api_url = 'https://model.cuspide.club/nearest-records'

        payload = {
            "criteria_ranges": {
                "Age": vector_input_ranges[0],
                "Years Active": vector_input_ranges[1],
                "Beauty": vector_input_ranges[2],
                "Skill Level": vector_input_ranges[3],
                "Award Wins": vector_input_ranges[4],
                "Media Mentions": vector_input_ranges[5],
                "Social Media Followers": vector_input_ranges[6],
                "Social Media Likes": vector_input_ranges[7],
                "Network Size": vector_input_ranges[8],
                "Income": vector_input_ranges[9]
            },
            "cat_variables": cat_variables
        }

        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            actores = data.get('closest_indices', [])
            return render_template('actores_encontrados.html', nearest_records=actores)
        else:
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return render_template('actores_encontrados.html', nearest_records=[])

    except Exception as e:
        print(f"Error: {str(e)}")  
        return render_template('actores_encontrados.html', nearest_records=[])


@app.route('/info_actor/<int:actor_id>', methods=['GET', 'POST'])
def info_actor(actor_id):
    actor_info = get_actor_info(actor_id)

    if request.method == 'POST':
        return guardar_favorito(actor_id)

    return render_template('info_actor.html', actor=actor_info) 

def get_actor_info(actor_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM actores WHERE id = %s", (actor_id,))
            actor_info = cursor.fetchone()
    return actor_info

@app.route('/misproyectos')
def misproyectos():
    if 'id' in session:  
        usuario_id = session['id']  
        proyectos = obtener_proyectos_por_usuario(usuario_id)  
        return render_template('misproyectos.html', proyectos=proyectos)
    return redirect(url_for('login'))  

def obtener_proyectos_por_usuario(usuario_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.id, 
                p.titulo, 
                p.descripcion, 
                p.genero, 
                p.fecha_inicio, 
                p.fecha_fin, 
                p.presupuesto,
                ARRAY_AGG(a.actor_id) AS actores_ids
            FROM proyectos p
            JOIN actividad a ON p.id = a.proyecto_id
            WHERE a.usuario_id = %s
            GROUP BY p.id
        """, (usuario_id,))
        proyectos = cursor.fetchall()
    return proyectos

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    actors = get_random_actors()
    discount = random.randint(70, 90)
    return render_template('menu.html', actors=actors, discount=discount)

def get_random_actors():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
         cursor.execute("SELECT * FROM actores ORDER BY RANDOM() LIMIT 4")
         actors = cursor.fetchall()
        return actors 

@app.route('/guardar_favorito/<int:actor_id>', methods=['POST'])
def guardar_favorito(actor_id):
    usuario_id = session.get('id')  
    if usuario_id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO favoritos (usuario_id, actor_id) VALUES (%s, %s)',
                (usuario_id, actor_id)
            )
            conn.commit()
            flash('Actor guardado en favoritos')
        except psycopg2.IntegrityError:
            flash('El actor ya está en tu lista de favoritos')
        except Exception as e:
            flash(f'Error al guardar el favorito: {str(e)}')
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Debes iniciar sesión para guardar favoritos')
    
    
    return redirect(url_for('info_actor', actor_id=actor_id))

@app.route('/info_proyecto/<int:proyecto_id>')
def info_proyecto(proyecto_id):
    proyecto_info = get_proyecto_info(proyecto_id)
    actores_relacionados = get_actores_relacionados(proyecto_id)
    return render_template('info_proyecto.html', proyecto=proyecto_info, actores=actores_relacionados)

def get_proyecto_info(proyecto_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM proyectos WHERE id = %s", (proyecto_id,))
            proyecto_info = cursor.fetchone()
    return proyecto_info

def get_actores_relacionados(proyecto_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT a.id, a.name, act.rol
                FROM actores a 
                JOIN actividad act ON a.id = act.actor_id 
                WHERE act.proyecto_id = %s
            """, (proyecto_id,))
            actores = cursor.fetchall()
    return actores

@app.route('/crear_proyecto', methods=['GET', 'POST'])
def crear_proyecto():
    user_id = session.get('id')  

    if user_id is None:
        return redirect(url_for('login'))  

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        genero = request.form['genero']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        presupuesto = request.form['presupuesto']
        actores_seleccionados = request.form.getlist('actores') 

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) FROM proyectos 
            WHERE titulo = %s AND descripcion = %s AND genero = %s 
            AND fecha_inicio = %s AND fecha_fin = %s AND presupuesto = %s
        """, (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto))
        count = cur.fetchone()[0]

        if count > 0:
            flash('Ya existe un proyecto exactamente igual. Por favor, modifica los detalles.', 'error')
            cur.close()
            conn.close()
            return redirect(url_for('crear_proyecto'))  # Redirigir para que el usuario pueda corregirlo

        
        cur.execute("""
            INSERT INTO proyectos (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto))
        
        proyecto_id = cur.fetchone()[0] 
        
        for actor_id in actores_seleccionados:
            cur.execute("""
                INSERT INTO actividad (usuario_id, proyecto_id, actor_id, rol, fecha_inicio)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, proyecto_id, actor_id, None, datetime.now()))
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('misproyectos'))  

    
    actores = get_favoritos(user_id) 

    return render_template('crear_proyecto.html', actores=actores)

@app.route('/eliminar_proyecto/<int:proyecto_id>', methods=['POST'])
def eliminar_proyecto(proyecto_id):
    user_id = session.get('id') 

    if user_id is None:
        return redirect(url_for('login'))  

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM actividad WHERE proyecto_id = %s
            """, (proyecto_id,))
            
            cur.execute("""
                DELETE FROM proyectos WHERE id = %s
            """, (proyecto_id,))
            
            conn.commit() 
            
            return redirect(url_for('misproyectos')) 
            
    except Exception as e:
        print("Error al eliminar el proyecto:", str(e))  
        return "Error al eliminar el proyecto: {}".format(str(e)), 500

@app.route('/misfavoritos')
def misfavoritos():
    usuario_id = session.get('id')  
    if not usuario_id:
        flash('Debes iniciar sesión para ver tus favoritos')
        return redirect(url_for('login'))  

    favoritos = get_favoritos(usuario_id)  
    return render_template('misfavoritos.html', actors=favoritos)

def get_favoritos(usuario_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.name, a.gender, a.genre_specialization
                FROM favoritos f
                JOIN actores a ON f.actor_id = a.id
                WHERE f.usuario_id = %s
            """, (usuario_id,))
            favoritos = cursor.fetchall()
    return favoritos

@app.route('/eliminar_favorito/<int:actor_id>', methods=['POST'])
def eliminar_favorito(actor_id):
    usuario_id = session.get('id') 
    if usuario_id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM favoritos WHERE usuario_id = %s AND actor_id = %s',
                (usuario_id, actor_id)
            )
            conn.commit()
            flash('Actor eliminado de favoritos')
        except Exception as e:
            flash(f'Error al eliminar el favorito: {str(e)}')
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Debes iniciar sesión para eliminar favoritos')

    return redirect(url_for('misfavoritos'))


if __name__ == '__main__':
    app.run(debug=True)
