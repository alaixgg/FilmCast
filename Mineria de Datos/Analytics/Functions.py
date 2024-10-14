#!/usr/bin/env python3
"""
Casting Inteligente: Algoritmos para la selección óptima de actores

Copyright (C) 2024  Alvarado Ludwig

Este archivo es parte de FilmCast.

FilmCast es software libre: puedes redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU tal como fue publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia o cualquier versión posterior.

FilmCast se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulta la Licencia Pública General de GNU para más detalles.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con FilmCast. Si no, consulta https://www.gnu.org/licenses/.
"""

import matplotlib.pyplot as plt
import pandas as pd

# Se carga el Dataset
def df_loader(ruta, separador):
  df = pd.read_csv(ruta, delimiter=separador)
  return df

def plotPie(categorical_column):
  category_counts = categorical_column.value_counts()

  plt.figure(figsize=(8, 8))
  plt.pie(
      category_counts,
      labels=category_counts.index,
      autopct='%1.1f%%',
      startangle=90
  )

  plt.show()

def plotScatter(df,x, y, x_title = "Eje $x$", y_title = "Eje $y$", title = "Título"):
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
    plt.scatter(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    return plt.show()

def plotBar(df,x, y, x_title = "Eje $x$", y_title = 'Eje $y$', title = 'Título'):
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
  plt.bar(x, y)
  plt.xlabel(x_title)
  plt.ylabel(y_title)
  plt.title(title)
  return plt.show()

def plotBox(df,var, x_title = 'Eje $x$', y_title = 'Eje $y$', title = 'Título'):
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
    plt.boxplot(var)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    return plt.show()
