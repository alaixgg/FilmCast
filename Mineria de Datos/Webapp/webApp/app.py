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
        usuario = request.form['usuario']
        clave = request.form['contrasena']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, clave, email, telefono, descripcion, Pais FROM usuarios WHERE nombre = %s AND clave = %s", (usuario, clave))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            session['id'] = resultado[0] 
            session['usuario'] = resultado[1]
            session['clave'] = resultado[2]
            session['email'] = resultado[3]
            session['telefono'] = resultado[4]
            session['descripcion'] = resultado[5]
            session['nacionalidad'] = resultado[6]
            
            return redirect(url_for('menu'))
        else:
            error = "Usuario o clave incorrectos."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario') 
        contrasena = request.form.get('contrasena')  
        confirmar_contrasena = request.form.get('confirmar_contrasena')

        if contrasena != confirmar_contrasena:
            error = "Las contraseñas no coinciden."
            return render_template('registro.html', error=error)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (usuario,))
        if cursor.fetchone():
            conn.close()
            error = "Ese nombre de usuario ya existe."
            return render_template('registro.html', error=error)

        cursor.execute("INSERT INTO usuarios (nombre, clave, descripcion, Pais, telefono, email) VALUES (%s, %s, %s, %s, %s, %s)",
                       (usuario, contrasena, '', '', '', ''))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/mensajes')
def mensajes():
    return render_template('mensajes.html')

@app.route('/perfil')
def perfil():
    if 'usuario' in session:
        return render_template('perfil.html', 
                               usuario=session['usuario'], 
                               descripcion=session.get('descripcion', ''),  
                               nacionalidad=session.get('nacionalidad', ''),
                               telefono=session.get('telefono', ''), 
                               email=session.get('email', ''))
    return redirect(url_for('login'))


@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario' in session:
        if request.method == 'POST':
            nuevo_telefono = request.form.get('telefono')
            nuevo_email = request.form.get('email')
            nueva_descripcion = request.form.get('descripcion')
            nuevo_Pais = request.form.get('Pais')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuarios 
                SET telefono = %s, email = %s, descripcion = %s, Pais = %s 
                WHERE nombre = %s
            """, (nuevo_telefono, nuevo_email, nueva_descripcion, nuevo_Pais, session['usuario']))
            conn.commit()
            conn.close()

            session['telefono'] = nuevo_telefono
            session['email'] = nuevo_email
            session['descripcion'] = nueva_descripcion
            session['nacionalidad'] = nuevo_Pais

            return redirect(url_for('perfil'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT telefono, email, descripcion, Pais FROM usuarios WHERE nombre = %s", (session['usuario'],))
        usuario_data = cursor.fetchone()
        conn.close()

        return render_template('editar_perfil.html', 
                               telefono=usuario_data[0],
                               email=usuario_data[1],
                               descripcion=usuario_data[2],
                               Pais=usuario_data[3])
    
    return redirect(url_for('perfil'))


@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    return render_template('busqueda.html')

@app.route('/busqueda_filtro')
def busqueda_filtro():
    categorias = ["Age", "Years Active", "Beauty", "Skill Level", "Award Wins", "Media Mentions", "Social Media Followers", "Social Media Likes", "Network Size", "Income"]
    categorias_con_indices = list(enumerate(categorias))
    return render_template('busqueda_filtro.html', categorias_con_indices=categorias_con_indices)

@app.route('/consulta_actor', methods=['POST'])
def consulta_actor():
    try:
        # Suponiendo que el formulario tiene inputs con nombres 'range_0_min', 'range_0_max', ..., 'weight_0', ...
        vector_input_ranges = [
            [int(request.form[f'range_{i}_min']), int(request.form[f'range_{i}_max'])]
            for i in range(10)
        ]
        
        weights = [
            int(request.form[f'weight_{i}'])
            for i in range(10)
        ]

        # URL de la API externa
        api_url = 'https://model.cuspide.club/nearest-records'  # Cambia a la URL de tu API

        # Datos para enviar en la solicitud
        payload = {
            "ranges": vector_input_ranges,
            "weights": weights
        }

        # Realizar la solicitud POST a la API externa
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            actores = data.get('nearest_records', [])
            print(actores)  # Imprimir los datos de actores para verificar
            return render_template('actores_encontrados.html', nearest_records=actores)
        else:
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return render_template('actores_encontrados.html', nearest_records=[])


    except Exception as e:
        print(f"Error: {str(e)}")  # Imprime el error
        return render_template('actores_encontrados.html', actores=[])




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
            SELECT p.id, p.titulo, p.descripcion, p.genero, p.fecha_inicio, p.fecha_fin, p.presupuesto 
            FROM proyectos p
            JOIN actividad a ON p.id = a.proyecto_id
            WHERE a.usuario_id = %s
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
        return redirect(url_for('login'))  # Redirigir a la página de login si no hay usuario autenticado

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        genero = request.form['genero']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        presupuesto = request.form['presupuesto']
        actores_seleccionados = request.form.getlist('actores')  # Captura de actores seleccionados

        conn = get_db_connection()
        cur = conn.cursor()

        # Comprobar si ya existe un proyecto con los mismos atributos
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

        # Insertar el nuevo proyecto en la tabla proyectos
        cur.execute("""
            INSERT INTO proyectos (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (titulo, descripcion, genero, fecha_inicio, fecha_fin, presupuesto))
        
        proyecto_id = cur.fetchone()[0] 
        
        # Insertar actores en la tabla actividad
        for actor_id in actores_seleccionados:
            cur.execute("""
                INSERT INTO actividad (usuario_id, proyecto_id, actor_id, rol, fecha_inicio)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, proyecto_id, actor_id, None, datetime.now()))
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('misproyectos'))  # Redirigir a la lista de proyectos

    # Obtener los actores favoritos para mostrarlos en el formulario
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
    usuario_id = session.get('id')  # Obtiene el ID del usuario desde la sesión
    if not usuario_id:
        flash('Debes iniciar sesión para ver tus favoritos')
        return redirect(url_for('login'))  # Redirige al inicio de sesión si no está autenticado

    favoritos = get_favoritos(usuario_id)  # Obtiene la lista de actores favoritos
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
    usuario_id = session.get('id')  # Obtiene el ID del usuario desde la sesión
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
