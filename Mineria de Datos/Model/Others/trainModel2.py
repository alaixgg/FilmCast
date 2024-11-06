#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import KFold
from sklearn.metrics import pairwise_distances

# Load the dataset
data = pd.read_csv('ActoresIndexOneHot.csv', sep=',')

# Define numerical variables
num_variables = ['Age', 'Years Active', 'Beauty', 'Skill Level', 'Award Wins',
                 'Media Mentions', 'Social Media Followers', 'Social Media Likes',
                 'Network Size', 'Income']

# Create a numpy array for the actor data using the original values
actor_data = data[num_variables].values

# Initialize KFold cross-validation with 5 splits
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Initialize lists to store results
all_mean_distances = []

# Perform K-fold cross-validation
for train_index, test_index in kf.split(actor_data):
    # Split the data into train and test sets
    X_train, X_test = actor_data[train_index], actor_data[test_index]

    # Initialize the KNN model
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')

    # Fit the KNN model on the training data
    knn.fit(X_train)

    # Find the nearest neighbors for the test set
    distances, indices = knn.kneighbors(X_test)

    # Calculate the mean distance for this fold
    mean_distance = np.mean(distances)
    all_mean_distances.append(mean_distance)

# Calculate the overall mean distance across all folds
overall_mean_distance = np.mean(all_mean_distances)

print(f"Overall Mean Distance: {overall_mean_distance}")
