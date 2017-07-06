# coding=utf-8
"""
Alumnos: De Giacomo - Ponce
Padrones: 99702 - 99723
Corrector: Agustina Mendez
"""
import sys


class BColors:
    """Colores para imprimir en la temrinal."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def imprimir_comando(comando, *args):
    """
    Imprime un comando con sus parametros.
    :param comando: String - comando.
    :param args: List<String> - Parametros a imprimir.
    """
    print(BColors.OKBLUE + "Comando:" + BColors.ENDC, comando)
    print(BColors.OKBLUE + "Parametros: " + BColors.ENDC, end=" ")
    print(" ".join(map(str, args)))
    print(BColors.OKBLUE + "Resultado:" + BColors.ENDC)


def imprimir_nodos(lista):
    """
    Recibe una lista de nodos y los imprime separados por comas.
    :param lista: List<Int> - Lista de nodos.
    """
    print(", ".join(map(str, lista)), end="\n\n")


def imprimir_camino(lista):
    """
    Recibe una lista de nodos y los imprime como un camino.
    :param lista: List<Int> - Lista de nodos.
    """
    print(" --> ".join(map(str, lista)), end="\n\n")


def imprimir_error(mensaje):
    """
    Imprime un mensaje de error.
    :param mensaje: String - Mensaje de error.
    """
    print(BColors.FAIL + "Error:" + BColors.ENDC, mensaje, file=sys.stderr, end="\n\n")


def imprimir_distancias(distancias):
    """
    Imprime la cantidad de nodos a cada nivel del un vertice.
    :param distancias: Map<Int, String> - Mapa con una lista de ids de vertices para cada distancia.
    """
    for k, v in distancias.items():
        print(k, ":", len(v))

    print("", end="\n\n")


def imprimir_mensaje(mensaje):
    """
    Imprime un mensaje en salida estandar.
    :param mensaje: String - Mensaje a imprimir.
    """
    print(mensaje, end="\n\n")


def imprimir_estadisticas(vertices, aristas):
    """
    Imprime las estadísticas (Cantidad de vértices, Cantidad de aristas, Promedio de grado de entrada de cada vértice,
    Promedio de grado de entrada de cada vértice, Densidad del grafo).
    :param vertices: Int - Cantidad de vertices.
    :param aristas: Int - Cantidad de aristas.
    """
    print("Cantidad de vértices:", vertices)
    print("Cantidad de aristas:", aristas)
    print("Promedio de grado de entrada de cada vértice:", vertices / aristas)
    print("Promedio de grado de salida de cada vértice:", vertices / aristas)
    print("Densidad del grafo:", 2*aristas / (vertices * (vertices - 1)), end="\n\n")


def imprimir_comunidad(comunidad, integrantes):
    """
    Imrpime los labels de las comunidades, la cantidad de integrantes y la lista de los integrantes.
    :param comunidad: String - Label de la comunidad.
    :param integrantes: List<String> - Ids de los vertices que integran la comunidad.
    """
    print("Comunidad", comunidad, " --> Integrantes:", len(integrantes), "-->", integrantes)
    print("", end="\n\n")
