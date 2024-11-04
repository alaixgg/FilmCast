#!/usr/bin/env python3

import pandas as pd
import numpy as np
import joblib
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler


data = pd.read_csv('ActoresIndexOneHot.csv', sep=',')

num_variables = ['Age', 'Years Active', 'Beauty', 'Skill Level', 'Award Wins', 'Media Mentions', 'Social Media Followers', 'Social Media Likes', 'Network Size', 'Income']
cat_variables = ['Gender_Female', 'Gender_Male', 'Nationality_Canada', 'Nationality_USA',
                 'Genre Specialization_Action', 'Genre Specialization_Comedy',
                 'Genre Specialization_Drama', 'Genre Specialization_Horror',
                 'Genre Specialization_Musical', 'Genre Specialization_Sci-Fi',
                 'Education Level_College', 'Education Level_Graduate',
                 'Education Level_High School', 'Education Level_University']
# Define the target ranges based on the criteria provided by the user
predecir = {
    "Age": (47, 48),
    "Years Active": (18, 19),
    "Beauty": (7, 8),
    "Skill Level": (9, 10),
    "Award Wins": (10, 11),
    "Media Mentions": (37, 38),
    "Social Media Followers": (18420, 18421),
    "Social Media Likes": (5378, 5379),
    "Network Size": (22, 23),
    "Income": (1188216, 1188220)
}


normalized_query_point = []

# Assume that num_variables are predefined
num_variables = list(predecir.keys())

# Normalize each feature from the dataset based on the provided criteria_ranges
scaled_actor_data = np.empty_like(data[num_variables].values)

for i, (feature, rng) in enumerate(predecir.items()):
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


# Initialize the KNN model to find 5 neighbors using weighted Euclidean distance
knn = NearestNeighbors(n_neighbors=5, metric='euclidean')

# Fit the KNN model to the scaled (weighted) actor data
knn.fit(scaled_actor_data)

joblib.dump(knn, 'knn_model.pkl')

# Find the 5 nearest neighbors based on the weighted query point
distances, indices = knn.kneighbors(normalized_query_point)

# Retrieve the closest records based on the indices
closest_records_sklearn = data.iloc[indices[0]][['Index'] + num_variables]

closest_records_sklearn
