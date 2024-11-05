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
            response = requests.post('https://db.cuspide.club/login', json=payload)
            response.raise_for_status()
            resultado = response.json()

            print("Respuesta del servidor:", resultado)
            token = resultado.get('token')
            print("Token recibido:", token)  

            if token:
                session['token'] = token
                session['id'] = resultado.get('id')
                session['usuario'] = resultado.get('nombre')
                session['email'] = resultado.get('email')
                session['telefono'] = resultado.get('telefono')
                session['descripcion'] = resultado.get('descripcion')
                session['nacionalidad'] = resultado.get('Pais')
                print("Token guardado en la sesión:", session.get('token'))

                return redirect(url_for('menu'))
            else:
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
            nombre = usuario_info.get('nombre', '')
            email = usuario_info.get('email', '')
            telefono = usuario_info.get('telefono', '')
            descripcion = usuario_info.get('descripcion', '')
            nacionalidad = usuario_info.get('nacionalidad', '')

            session['id'] = id
            session['nombre'] = nombre
            session['email'] = email
            session['telefono'] = telefono
            session['descripcion'] = descripcion
            session['nacionalidad'] = nacionalidad
            
            return render_template('perfil.html',
                                   id=id,
                                   nombre=nombre,
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
    if 'token' in session:
        token = session.get('token') 
        mensaje = session.get('mensaje') 
        print(mensaje) 

        if request.method == 'POST':
            nuevo_telefono = request.form.get('telefono')
            nuevo_email = request.form.get('email')
            nueva_descripcion = request.form.get('descripcion')
            nuevo_pais = request.form.get('Pais') 

            payload = {
                'telefono': nuevo_telefono,
                'email': nuevo_email,
                'descripcion': nueva_descripcion,
                'Pais': nuevo_pais  
            }
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            try:
                response = requests.post('https://db.cuspide.club/editar_perfil', json=payload, headers=headers)
                response.raise_for_status()  

                session['telefono'] = nuevo_telefono
                session['email'] = nuevo_email
                session['descripcion'] = nueva_descripcion
                session['nacionalidad'] = nuevo_pais

                
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
        return render_template('actores_sin_filtro.html', nearest_records=[])

@app.route('/busqueda_filtro')
def busqueda_filtro():
    categorias_numericas = [
        "Age", "Years Active", "Beauty", "Skill Level", 
        "Award Wins", "Media Mentions", "Social Media Followers", 
        "Social Media Likes", "Network Size", "Income"
    ]
    categorias_numericas_con_indices = list(enumerate(categorias_numericas))
    
    return render_template('busqueda_filtro.html', 
                           categorias_numericas_con_indices=categorias_numericas_con_indices)

@app.route('/consulta_actor', methods=['POST'])
def consulta_actor():
    try:
        if 'token' in session:
            token = session.get('token')
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        else:
            return render_template('actores_encontrados.html', nearest_records=[], error="Token de autenticación no encontrado.")


        vector_input_ranges = {}
        for i, categoria in enumerate(["Age", "Years Active", "Beauty", "Skill Level", 
                                       "Award Wins", "Media Mentions", "Social Media Followers", 
                                       "Social Media Likes", "Network Size", "Income"]):
            range_value = request.form.get(f'range_{i}')
            if range_value: 
                try:
                    min_val, max_val = map(int, range_value.split('-'))
                    vector_input_ranges[categoria] = [min_val, max_val]  
                except ValueError:
                    return render_template('actores_encontrados.html', nearest_records=[], error="Formato de rango no válido.")

        payload = {
            "predecir": vector_input_ranges
        }
        print(payload)

        api_url = 'https://model.cuspide.club/find_closest_actors'
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
            actores_ids = data.get('closest_indices', [])
            actores_info = []

  
            for actor_id in actores_ids:
                actor_info = get_actor_info(actor_id, headers)
                if actor_info:
                    actores_info.append(actor_info)

            return render_template('actores_encontrados.html', nearest_records=actores_info)
        else:
            error_message = f"Error al consultar actores: {response.status_code} - {response.text}"
            return render_template('actores_encontrados.html', nearest_records=[], error=error_message)

    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('actores_encontrados.html', nearest_records=[], error="Ocurrió un error en la consulta.")

    
def get_random_actors():
    actors = [] 

    if 'token' in session:
        token = session.get('token')
        headers = {
            'Authorization': f'Bearer {token}'
        }

        api_url = "https://db.cuspide.club/destacados"
        
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            actors = response.json()
            print(actors)
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP: {http_err} - Respuesta del servidor: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener actores destacados: {e}")

    else:
        print("No se encontró un token en la sesión.")
    
    return actors


@app.route('/menu')
def menu():
    actors = get_random_actors()
    return render_template('menu.html', actors=actors)


@app.route('/info_actor/<int:actor_id>', methods=['GET', 'POST']) 
def info_actor(actor_id):
    if 'token' not in session:
        app.logger.warning("Token no proporcionado en la sesión")
        return jsonify({"error": "Token no proporcionado en la sesión"}), 401

    token = session.get('token')
    headers = {'Authorization': f'Bearer {token}'}

    app.logger.info(f"Obteniendo información del actor con ID: {actor_id}")
    actor_info = get_actor_info(actor_id, headers)
    if actor_info is None:
        app.logger.warning(f"No se encontró información para el actor con ID: {actor_id}")
        return jsonify({"error": "Actor no encontrado"}), 404

    if request.method == 'POST':
        return guardar_favorito(actor_id)

    return render_template('info_actor.html', actor=actor_info)


def get_actor_info(actor_id, headers):
    try:
        response = requests.get(f'https://db.cuspide.club/info_actor/{actor_id}', headers=headers)
        response.raise_for_status()
        return response.json()
        print(response.json())
    except requests.exceptions.RequestException as err:
        app.logger.error(f"Error al obtener la información del actor: {err}")
        return None

@app.route('/guardar_favorito/<int:actor_id>', methods=['POST'])
def guardar_favorito(actor_id):
    usuario_id = session.get('id')
    
    if 'token' in session:
        token = session.get('token')
        headers = {
            'Authorization': f'Bearer {token}'
        }

        api_url = f"https://db.cuspide.club/guardar_favorito/{actor_id}"
        try:
            response = requests.post(api_url, headers=headers)
            response.raise_for_status()  

            flash('Actor guardado en favoritos')
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 409:
                flash('El actor ya está en tu lista de favoritos')
            else:
                flash(f'Error al guardar el favorito: {str(err)}')
        except Exception as e:
            flash(f'Error al guardar el favorito: {str(e)}')
    else:
        flash('Debes iniciar sesión para guardar favoritos')

    return redirect(url_for('info_actor', actor_id=actor_id))

@app.route('/misproyectos')
def misproyectos():
    if 'id' in session and 'token' in session:
        usuario_id = session['id']
        token = session['token']
        proyectos = obtener_proyectos_por_usuario(usuario_id, token)
        
        proyectos_unicos = []
        titulos_vistos = set()

        for proyecto in proyectos:
            titulo = proyecto.get('titulo') 
            if titulo not in titulos_vistos:
                proyectos_unicos.append(proyecto)
                titulos_vistos.add(titulo)

        return render_template('misproyectos.html', proyectos=proyectos_unicos)
    return redirect(url_for('login'))

def obtener_proyectos_por_usuario(usuario_id, token):
    url = "https://db.cuspide.club/mis_proyectos"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        proyectos = response.json()
        return proyectos
    except requests.RequestException as e:
        print(f"Error al obtener los proyectos: {e}")
        return []


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/info_proyecto/<int:proyecto_id>')
def info_proyecto(proyecto_id):
    if 'token' in session:  
        token = session['token']
        proyecto_info = get_proyecto_info(proyecto_id, token)
        actores_relacionados = get_actores_relacionados(proyecto_id, token)
        return render_template('info_proyecto.html', proyecto=proyecto_info, actores=actores_relacionados)
    return redirect(url_for('login'))

def get_proyecto_info(proyecto_id, token):
    url = f"https://db.cuspide.club/info_proyecto/{proyecto_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        proyecto_info = response.json()
        
   
        unique_info = set()
        
        for key, value in proyecto_info.items():
            if value not in unique_info:
                print(f"{key}: {value}")
                unique_info.add(value)
        
        return proyecto_info

    except requests.RequestException as e:
        print(f"Error al obtener la información del proyecto: {e}")
        return None


def get_actores_relacionados(proyecto_id, token):
    
    url = f"https://db.cuspide.club/actores_relacionados/{proyecto_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        actores = response.json()
        return actores
    except requests.RequestException as e:
        print(f"Error al obtener actores relacionados: {e}")
        return []
    
@app.route('/crear_proyecto', methods=['GET', 'POST'])
def crear_proyecto():
    user_id = session.get('id')  

    if user_id is None:
        return redirect(url_for('login'))  

  
    token = session.get('token')  

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        genero = request.form['genero']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        presupuesto = request.form['presupuesto']
        actores_seleccionados = request.form.getlist('actores') 

        data = {
            'titulo': titulo,
            'descripcion': descripcion,
            'genero': genero,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'presupuesto': presupuesto,
            'actores_seleccionados': actores_seleccionados
        }

        try:
        
            response = requests.post('https://db.cuspide.club/crear_proyecto', json=data, headers=headers, timeout=10)
            response.raise_for_status()  
            
            if response.status_code == 201: 
                return redirect(url_for('misproyectos'))  
            else:
                flash(response.json().get('error', 'Error desconocido'), 'error')

        except requests.exceptions.Timeout:
            flash('La solicitud ha superado el tiempo de espera. Intente nuevamente.', 'error')
        except requests.exceptions.RequestException as e:
            flash(f'Ocurrió un error: {e}', 'error')

        return redirect(url_for('crear_proyecto'))  

    actores = get_favoritos(user_id, headers)
    return render_template('crear_proyecto.html', actores=actores)

@app.route('/eliminar_proyecto/<int:proyecto_id>', methods=['POST'])
def eliminar_proyecto(proyecto_id):
    user_id = session.get('id')
    token = session.get('token')

    if user_id is None:
        return redirect(url_for('login'))

    response = requests.post(f'https://db.cuspide.club/eliminar_proyecto/{proyecto_id}', headers={'Authorization': f'Bearer {token}'})

    if response.status_code == 200:
        return redirect(url_for('misproyectos'))
    else:
        print("Error al eliminar el proyecto:", response.text)
        return "Error al eliminar el proyecto: {}".format(response.text), 500

@app.route('/misfavoritos', methods=['GET'])
def misfavoritos():
    usuario_id = session.get('id')
    print('ID de usuario:', usuario_id)

    if not usuario_id:
        flash('Debes iniciar sesión para ver tus favoritos')
        return redirect(url_for('login'))

    headers = {}
    if 'token' in session:
        token = session.get('token')
        headers['Authorization'] = f'Bearer {token}'
    else:
        flash('No se encontró el token. Por favor, inicia sesión de nuevo.')
        return redirect(url_for('login'))

    favoritos = get_favoritos(usuario_id, headers)

    if not favoritos: 
        flash('No tienes actores favoritos.')

    return render_template('misfavoritos.html', actors=favoritos)
def get_favoritos(usuario_id, headers):
    response = requests.get('https://db.cuspide.club/mis_favoritos', headers=headers)

    if response.status_code == 200:
        return response.json() 
    else:
        flash('Error al obtener favoritos: {}'.format(response.text))
        return [] 
 

@app.route('/eliminar_favorito/<int:actor_id>', methods=['POST'])
def eliminar_favorito(actor_id):
    usuario_id = session.get('id')
    token = session.get('token')

    if usuario_id:
        try:
            response = requests.post(f'https://db.cuspide.club/eliminar_favorito/{actor_id}', 
                                     headers={'Authorization': f'Bearer {token}'})

            if response.status_code == 200:
                flash('Actor eliminado de favoritos')
            else:
                flash('Error al eliminar el favorito: {}'.format(response.text))
        except Exception as e:
            flash(f'Error al eliminar el favorito: {str(e)}')
    else:
        flash('Debes iniciar sesión para eliminar favoritos')

    return redirect(url_for('misfavoritos'))



if __name__ == '__main__':
    app.run(debug=True)
