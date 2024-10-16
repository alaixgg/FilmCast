#!/usr/bin/env Librerias
# python
from sklearn.neighbors import NearestNeighbors
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Importar el dataset
df = pd.read_csv("../Datasets/Actores.csv", sep=";")
# Eliminar duplicados del dataset
df = df.drop_duplicates()
# Crear un dataframe únicamente con variables numéricas
dfNum = df.select_dtypes(include=[np.number])

# Crear una matriz X a partir de los valores del df numérico
X = dfNum.values

# Este vector es lo que deja el usuario a colocar (Age, Years Active, Beauty, Skill Level, Award Wins, Media Mentions Social Media Followers, Social Media Likes, Network Size, Income)
vector_input_ranges = [(20, 30), (5, 15), (9, 15), (2, 10), (5, 10), (20, 40), (15000, 20000), (4000, 5000), (20, 30), (200000, 220000)]

# Define qué tan importante es el atributo de acuerdo a lo que escoge el director.
weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Dado un record del dataframe calcula la distancia comparado a los rangos y ajustado a los pesos.
def custom_weighted_distance_with_ranges(record, ranges, weights):
    # Representa qué tan lejos el registro está de los rangos.
    total_distance = 0
    # Se itera sobre cada variable del registro, junto con el correspondiente rango
    for i, (low, high) in enumerate(ranges):
        # Valor de la columna i del registro que se tomó
        value = record[i]
        # Si el valor está en el rango, no se agrega distancia
        if low <= value <= high:
            dist = 0
        else:
            # Si el valor está por fuera del rango que se dio, calcula qué tal lejos está el valor de la frontera más cercana.
            dist = min(abs(low - value), abs(high - value))

        total_distance += weights[i] * dist

    return total_distance

# Encuentra los 5 registros más cercanos basados en la distancia entre cada registro y un conjunto de rangos numéricos
def find_nearest_neighbors_by_ranges(X, vector_input_ranges, weights, k=5):
    # Almacena la distancia entre los rangos de entrada y cada registro en el dataset.
    distances = []

    # Distancia de vector_input_ranges y cada registro del dataset
    for record in X:
        dist = custom_weighted_distance_with_ranges(record, vector_input_ranges, weights)
        distances.append(dist)

    # Obtiene la lista de los 5 indices por distancia, desde la más chiquita hasta la más grande.
    nearest_indices = np.argsort(distances)[:k]

    return nearest_indices

@app.route('/nearest-records', methods=['GET', 'POST'])
def nearest_records():
    try:
        data = request.jso

        vector_input_ranges = data['ranges']
        weights = data['weights']

        nearest_indices = find_nearest_neighbors_by_ranges(X, vector_input_ranges, weights, k=5)

        nearest_record = df.iloc[nearest_indices].to_dict(orient='records')

        return jsonify({"message": "Success", "nearest_records": nearest_record}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

# Encuentra los valores más cercanos de acuerdo a vector_input_ranges definido más arriba, junto con los weights
# que también se definieron arriba.
# nearest_neighbors_indices =

# print("Los 5 registros que más se asemejan son:")
# for neighbor in nearest_neighbors_indices:
#     print(f"Registro en el index {neighbor}:")
#     print(df.iloc[neighbor].Name)  # Muestra el nombre del registro que más se acerca
