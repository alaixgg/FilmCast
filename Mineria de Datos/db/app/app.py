#!/usr/bin/env python
"""
Casting Inteligente: Algoritmos para la selección óptima de actores

Copyright (C) 2024  Alvarado Ludwig

Este archivo es parte de FilmCast.

FilmCast es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal como fue publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia o cualquier versión posterior.

FilmCast se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con FilmCast. Si no, consulta https://www.gnu.org/licenses/.
"""

import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Use a fallback key if SECRET_KEY is not set

redis_client = Redis(host='redis', port=6379)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379"  # Use service name as host
)
limiter.init_app(app)

from token_mod import generate_token, token_required
from conn_mod import get_db_connection
from auth_mod import post_login, post_register
from end_usuarios import get_perfil,post_perfil
from end_actors import get_actor,get_destacados

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)