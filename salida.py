# coding=utf-8
"""
Alumnos: De Giacomo - Ponce
Padrones: 99702 - 99723
Corrector: Agustina Mendez
"""
from __future__ import print_function

import sys


# todo las funciones para imprimir nodos repiten codigo
def imprimir_comando(comando, *args):
    """
    Imprime un comando con sus parametros
    :param comando: String - comando
    :param args: List<String> - Parametros a imprimir
    """
    print(comando, end=" ")
    print(" ".join(map(str, args)))


def imprimir_nodos(lista):
    """
    Recibe una lista de nodos y los imprime separados por comas
    :param lista: List<Int> - Lista de nodos
    """
    print(", ".join(map(str, lista)), end="\n\n")


def imprimir_camino(lista):
    """
    Recibe una lista de nodos y los imprime como un camino
    :param lista: List<Int> - Lista de nodos
    """
    print(" --> ".join(map(str, lista)), end="\n\n")


def imprimir_error(mensaje):
    """
    Imprime un mensaje de error
    :param mensaje: String - Mensaje de error
    """
    print("Error: " + mensaje, file=sys.stderr, end="\n\n")


def imprimir_distancias(distancias):
    """
    Imprime la cantidad de nodos a cada nivel del un vertice
    :param distancias: Map<Int, Int> - Mapa con una lista de nodos para cada distancia
    """
    for k, v in distancias.items():
        print(str(k) + ": " + str(len(v)))

    print("", end="\n\n")


def imprimir_mensaje(mensaje):
    """
    Imprime un mensaje en salida estandar
    :param mensaje: String - Mensaje a imprimir
    """
    print(mensaje, end="\n\n")


def imprimir_estadisticas(vertices, aristas):
    """
    Imprime las estadísticas (Cantidad de vértices, Cantidad de aristas, Promedio de grado de entrada de cada vértice,
    Promedio de grado de entrada de cada vértice, Densidad del grafo)
    :param vertices: Int - Cantidad de vertices
    :param aristas: Int - Cantidad de aristas
    """
    print("Cantidad de vértices: " + str(vertices))
    print("Cantidad de aristas: " + str(aristas))
    print("Promedio de grado de entrada de cada vértice: " + str(vertices / aristas))
    print("Promedio de grado de entrada de cada vértice: " + str(vertices / aristas))
    print("Densidad del grafo: " + str(aristas / (vertices * (vertices - 1))))
