#!/usr/bin/env python3
"""
Casting Inteligente: Algoritmos para la selección óptima de actores

Copyright (C) 2024  Alvarado Ludwig

Este archivo es parte de FilmCast.

FilmCast es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal como fue publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia o cualquier versión posterior.

FilmCast se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con FilmCast. Si no, consulta https://www.gnu.org/licenses/.


TODO:
- Agregar variables categóricas.
- Retornar el ID de 5 actores.
- Revisar la normalización.
"""



from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import euclidean
import pandas as pd
import numpy as np

data = pd.read_csv('ActoresFilter.csv', sep=',')

# Define the normalized target ranges based on the criteria provided by the user
# These ranges are derived directly from the user's specifications.
criteria_ranges = {
    "Age": (47, 48),
    "Years Active": (18, 19),
    "Beauty": (7, 8),
    "Skill Level": (9, 10),
    "Award Wins": (10, 11),
    "Media Mentions": (37, 38),
    "Social Media Followers": (18420, 18421),
    "Social Media Likes": (5378, 5379),
    "Network Size": (30, 31),
    "Income": (1188216, 1188220)
}

# Calculate midpoints of each range as the "target" value
target_values = {feature: (rng[0] + rng[1]) / 2 for feature, rng in criteria_ranges.items()}

# Select the columns of interest from the dataset for KNN
features = list(criteria_ranges.keys())
actor_data = data[features]

# Normalize the target values in the same range as the data
min_values = actor_data.min()
max_values = actor_data.max()
normalized_target_values = [(target_values[feature] - min_values[feature]) / (max_values[feature] - min_values[feature])
                            for feature in features]

# Calculate Euclidean distances from each actor's data to the target normalized values
distances = actor_data.apply(lambda row: euclidean(row, normalized_target_values), axis=1)

# Add the distances to the data and sort by distance
data['Distance'] = distances
closest_records = data.nsmallest(5, 'Distance')

# Display the 5 closest records
print(closest_records[features + ['Distance']])



# # Initialize the KNN model from sklearn
# # We'll set it up to find 5 neighbors based on Euclidean distance
# knn = NearestNeighbors(n_neighbors=5, metric='euclidean')

# # Fit the model to the normalized data
# knn.fit(actor_data)

# # Use the normalized target values as the query for finding neighbors
# query_point = np.array(normalized_target_values).reshape(1, -1)

# # Find the 5 nearest neighbors based on the query point
# distances, indices = knn.kneighbors(query_point)

# # Retrieve the closest records based on the indices
# closest_records_sklearn = data.iloc[indices[0]][features + ['Distance']]

# # Display the closest records with distances
# closest_records_sklearn
