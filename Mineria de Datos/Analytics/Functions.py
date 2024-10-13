#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Se carga el Dataset
df = pd.read_csv('../Datasets/Actores.csv', delimiter=';')

def plotScatter(x, y, x_title = "Eje $x$", y_title = "Eje $y$", title = "Título"):
    """
    Función para hacer un scatter más rápido.
    Args:
      x:          type: str   Desc: Debe ser una variable que esté como columna dentro del DataFrame y numérica.
      y:          type: str   Desc: Debe ser una variable que esté como columna dentro del DataFrame y numérica.
      x_title:    type: str   Desc: Texto para el eje x, el valor por defecto es "Eje x".
      y_title:    type: str   Desc: Texto para el eje y, el valor por defecto es "Eje y".
      title:      type: str   Desc: Texto para el título del plot, el valor por defecto es "Título".
    Returns:
      Gráfico de dispersión de las variables (x, y) que se indiquen.
    """
    plt.scatter(df[x], df[y])
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    return plt.show()

def plotBar(x, y, x_title = "Eje $x$", y_title = 'Eje $y$', title = 'Título'):
  """
    Función para hacer un gráfico de barras más rápido.
    Args:
      x:          type: str   Desc: Debe ser una variable que esté como columna dentro del DataFrame y categórica.
      y:          type: str   Desc: Debe ser una variable que esté como columna dentro del DataFrame y numérica.
      x_title:    type: str   Desc: Texto para el eje x, el valor por defecto es "Eje x".
      y_title:    type: str   Desc: Texto para el eje y, el valor por defecto es "Eje y".
      title:      type: str   Desc: Texto para el título del plot, el valor por defecto es "Título".
    Returns:
      Gráfico de barras para las variables (x, y) que se indiquen.
    """
  plt.bar(df[x], df[y])
  plt.xlabel(x_title)
  plt.ylabel(y_title)
  plt.title(title)
  return plt.show()

def plotBox(var, x_title = 'Eje $x$', y_title = 'Eje $y$', title = 'Título'):
    """
    Función para hacer un gráfico de caja más rápido.

    Args:
      var:        type: str   Desc: Debe ser una variable que esté como columna dentro del DataFrame y numérica.
      x_title:    type: str   Desc: Texto para el eje x, el valor por defecto es "Eje x".
      y_title:    type: str   Desc: Texto para el eje y, el valor por defecto es "Eje y".
      title:      type: str   Desc: Texto para el título del plot, el valor por defecto es "Título".
    Returns:
      Gráfico de cajas para una variable "var"
    """
    plt.boxplot(df[var])
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    return plt.show()
