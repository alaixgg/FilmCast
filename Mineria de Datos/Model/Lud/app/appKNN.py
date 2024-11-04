#!/usr/bin/env python3

"""
Casting Inteligente: Algoritmos para la selección óptima de actores

Copyright (C) 2024  Alvarado Ludwig

Este archivo es parte de FilmCast.

FilmCast es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal como fue publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia o cualquier versión posterior.

FilmCast se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con FilmCast. Si no, consulta https://www.gnu.org/licenses/.

TODO:
- Hacer que funcione con categóricas.
"""

import os
from flask import Flask, request, jsonify
import jwt
import bcrypt
import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql.cursors
from redis import Redis
import time
import logging
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv('ActoresIndexOneHot.csv', sep=',')

# Define the target ranges based on the criteria provided by the user
# criteria_ranges = {
#     "Age": (47, 48),
#     "Years Active": (18, 19),
#     "Beauty": (7, 8),
#     "Skill Level": (9, 10),
#     "Award Wins": (10, 11),
#     "Media Mentions": (37, 38),
#     "Social Media Followers": (18420, 18421),
#     "Social Media Likes": (5378, 5379),
#     "Network Size": (22, 23),
#     "Income": (1188216, 1188220)
# }

# # Define weights for each feature (higher weight means higher priority)
# weights = {
#     "Age": 0.5,
#     "Years Active": 0.7,
#     "Beauty": 0.5,
#     "Skill Level": 2.0,
#     "Award Wins": 1.5,
#     "Media Mentions": 1.0,
#     "Social Media Followers": 0.8,
#     "Social Media Likes": 0.8,
#     "Network Size": 100.0,
#     "Income": 0.7
# }

num_variables = ['Age', 'Years Active', 'Beauty', 'Skill Level', 'Award Wins', 'Media Mentions', 'Social Media Followers', 'Social Media Likes', 'Network Size', 'Income']
cat_variables = ['Gender_Female', 'Gender_Male', 'Nationality_Canada', 'Nationality_USA',
                 'Genre Specialization_Action', 'Genre Specialization_Comedy',
                 'Genre Specialization_Drama', 'Genre Specialization_Horror',
                 'Genre Specialization_Musical', 'Genre Specialization_Sci-Fi',
                 'Education Level_College', 'Education Level_Graduate',
                 'Education Level_High School', 'Education Level_University']

# --------------------- API ---------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
redis_client = Redis(host='redis', port=6379)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379"
)
limiter.init_app(app)

# KNN search function
@app.route('/find_closest_actors', methods=['POST'])
def find_closest_actors():
    # Parse the incoming JSON request
    request_data = request.get_json()

    # Retrieve criteria_ranges and weights from the request
    criteria_ranges = request_data.get('criteria_ranges')
    weights = request_data.get('weights')

    if not criteria_ranges or not weights:
        return jsonify({"error": "Both criteria_ranges and weights must be provided."}), 400

    # Initialize a dictionary to store normalized query point values
    normalized_query_point = []

    # Assume that num_variables are predefined
    num_variables = list(criteria_ranges.keys())

    # Normalize each feature from the dataset based on the provided criteria_ranges
    scaled_actor_data = np.empty_like(data[num_variables].values)

    for i, (feature, rng) in enumerate(criteria_ranges.items()):
        # Initialize a MinMaxScaler for each feature's range
        scaler = MinMaxScaler()
        scaler.fit([[rng[0]], [rng[1]]])

        # Normalize the actor data for this feature
        scaled_actor_data[:, i] = scaler.transform(data[[feature]]).flatten()

        # Normalize the query value (target range midpoint)
        midpoint = np.array([[(rng[0] + rng[1]) / 2]])
        normalized_query_point.append(scaler.transform(midpoint).flatten())

    # Convert the query point into a numpy array and reshape it for KNN
    normalized_query_point = np.array(normalized_query_point).reshape(1, -1)

    # Apply weights to both the scaled actor data and the query point
    for i, feature in enumerate(criteria_ranges.keys()):
        weight = weights[feature]
        scaled_actor_data[:, i] *= weight  # Scale the actor data by the feature weight
        normalized_query_point[:, i] *= weight  # Scale the query point by the feature weight

    # Initialize the KNN model to find 5 neighbors using weighted Euclidean distance
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')

    # Fit the KNN model to the scaled (weighted) actor data
    knn.fit(scaled_actor_data)

    # Find the 5 nearest neighbors based on the weighted query point
    distances, indices = knn.kneighbors(normalized_query_point)

    # Retrieve the closest records based on the indices
    closest_records_sklearn = data.iloc[indices[0]][['Index'] + num_variables]

    # Return the closest records' indices as a response
    return jsonify({"closest_indices": closest_records_sklearn['Index'].to_numpy().tolist()})

@app.route('/find_closest_actors', methods=['GET'])
@limiter.limit("5 per minute")  # Limit requests to prevent abuse
def closest_actors_endpoint():
    closest_indices = find_closest_actors()
    return jsonify({"closest_indices": closest_indices.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
