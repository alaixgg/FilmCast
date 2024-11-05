#!/usr/bin/env python3

import pandas as pd
import numpy as np
import joblib
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv('ActoresIndexOneHot.csv', sep=',')

num_variables = ['Age', 'Years Active', 'Beauty', 'Skill Level', 'Award Wins',
                 'Media Mentions', 'Social Media Followers', 'Social Media Likes',
                 'Network Size', 'Income']
cat_variables = ['Gender_Female', 'Gender_Male', 'Nationality_Canada',
                 'Nationality_USA', 'Genre Specialization_Action',
                 'Genre Specialization_Comedy', 'Genre Specialization_Drama',
                 'Genre Specialization_Horror', 'Genre Specialization_Musical',
                 'Genre Specialization_Sci-Fi', 'Education Level_College',
                 'Education Level_Graduate', 'Education Level_High School',
                 'Education Level_University']

# Define the target ranges based on the criteria provided by the user
predecir = {
    "Age": (30, 35),
    "Years Active": (5, 10),
    "Beauty": (5, 7),
    "Skill Level": (6, 8),
    "Award Wins": (2, 4),
    "Media Mentions": (20, 30),
    "Social Media Followers": (1000, 5000),
    "Social Media Likes": (100, 300),
    "Network Size": (10, 15),
    "Income": (50000, 100000)
}


# Create a numpy array for the actor data using the original values
actor_data = data[num_variables].values

# Initialize the KNN model to find 5 neighbors using the default Euclidean distance
knn = NearestNeighbors(n_neighbors=5, metric='euclidean')

# Fit the KNN model to the original actor data
knn.fit(actor_data)

# Save the KNN model
joblib.dump(knn, 'knn_model.pkl')

# To find the closest actors, calculate the midpoint of the target ranges
normalized_query_point = []

for feature, rng in predecir.items():
    midpoint = (rng[0] + rng[1]) / 2
    normalized_query_point.append(midpoint)

# Convert the query point into a numpy array and reshape it for KNN
normalized_query_point = np.array(normalized_query_point).reshape(1, -1)

# Find the 5 nearest neighbors based on the query point
distances, indices = knn.kneighbors(normalized_query_point)

# Retrieve the closest records based on the indices
closest_records_sklearn = data.iloc[indices[0]][['Index'] + num_variables]

print(closest_records_sklearn)
