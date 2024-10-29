from flask import Flask, session, redirect, url_for, render_template, request
import pandas as pd 
from openpyxl import Workbook
import os 
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
    return render_template('busqueda_filtro.html')


#@app.route('/buscar_actores', methods=['POST'])
#def buscar_actores():
 #   age_range = request.form.get("age_range")
  #  years_active_range = request.form.get("years_active_range")
    #vector_input_ranges = [
     #   tuple(map(int, age_range.split('-'))),
    #    tuple(map(int, years_active_range.split('-'))),
        
    #
    #response = nearest_records(vector_input_ranges, [1] * len(vector_input_ranges))
    
   # return render_template('resultados_busqueda.html', records=response)

#def nearest_records(vector_input_ranges, weights):
#   nearest_indices = find_nearest_neighbors_by_ranges(X, vector_input_ranges, weights, k=5)
#  nearest_record = df.iloc[nearest_indices].to_dict(orient='records')
# return nearest_record



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

@app.route('/info_actor/<int:actor_id>')
def info_actor(actor_id):
    actor_info = get_actor_info(actor_id)
    return render_template('info_actor.html', actor=actor_info)

def get_actor_info(actor_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM actores WHERE id = %s", (actor_id,))
            actor_info = cursor.fetchone()
    return actor_info


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






if __name__ == '__main__':
    app.run(debug=True)
