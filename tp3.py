# coding=utf-8
"""
Alumnos: De Giacomo - Ponce
Padrones: 99702 - 99723
Corrector: Agustina Mendez
"""
import csv
from grafo import Grafo
import random
import heapq
from salida import *

N_WALKS = 100
WALKS_LARGE = 300
N_RANDOM_CHOICE = 20
LABEL_ITER = 10
LABEL_WALKS_LARGE = 30


def main():
    """
    Lee el archivo que recive en los argumentos y carga el grafo.
    Lee los comandos de a uno y ejecuta la función correspondiente.
    """

    if len(sys.argv) != 2:
        imprimir_error("-Please provide 1 arguments-")
        imprimir_error("-Usage: tp3.py <inputfile>")
        sys.exit(2)

    grafo = Grafo()

    imprimir_mensaje("Loading file ...")
    with open(sys.argv[1]) as file:
        for _ in range(4):
            next(file)
        reader = csv.DictReader(file, delimiter="\t", fieldnames=["a", "b"])
        for line in reader:
            grafo.agregar_vertice(line["a"])
            grafo.agregar_vertice(line["b"])
            grafo.agregar_arista(line["a"], line["b"])

    # Leo por entrada standard
    imprimir_mensaje("Reading commands ...")
    for line in sys.stdin:
        comando = line.split(" ")
        do_function(comando[0], comando[1:], grafo)


def do_function(command, args, grafo):
    # todo imprimir errores en la cantidad de argumentos
    # todo imprimir la salida tambien en esta funcion
    """
    Recibe un comando a ejecutar y llama a la función correspondiente.
    :param command: String - Comando a ejecutar.
    :param args: List<String> - Lista de parámetros para la ejecución del comando.
    :param grafo: Grafo - Grafo sobre el cual ejecutar el comando.
    """
    if command == "similares":
        imprimir_comando("similares", str(args[0]).rstrip(), int(args[1]))
        similares(grafo, str(args[0]).rstrip(), int(args[1]))
    if command == "recomendar":
        imprimir_comando("recomendar", str(args[0]).rstrip(), int(args[1]))
        recomendar(grafo, str(args[0]).rstrip(), int(args[1]))
    if command == "camino":
        imprimir_comando("camino", str(args[0]).rstrip(), str(args[1]).rstrip())
        camino(grafo, str(args[0]).rstrip(), str(args[1]).rstrip())
    if command == "centralidad_exacta":
        imprimir_comando("centralidad_exacta", int(args[0]))
        centralidad_exacta(grafo, int(args[0]))
    if command == "centralidad_aproximada":
        imprimir_comando("centralidad_aproximada", int(args[0]))
        centralidad_aproximada(grafo, int(args[0]))
    if command == "distancias":
        imprimir_comando("distancias", str(args[0]).rstrip())
        distancias(grafo, str(args[0]).rstrip())
    if command == "estadisticas":
        imprimir_comando("estadisticas")
        estadisticas(grafo)
    if command == "comunidades":
        imprimir_comando("comunidades")
        comunidades(grafo)


# Tiempo: random walks (lineal) + n mayores con heap (n*log(k)) n->Cantidad de nodos total de todos los recorridos
def similares(grafo, vertice, k):
    """
    Dado un vertice, encuentra los vertices más similares a este.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id de un vertice.
    :param k: Int - Cantidad de similares a buscar.
    """
    aux = n_random_walks(grafo, vertice, N_WALKS, WALKS_LARGE)
    lista = heapq.nlargest(k, aux, key=aux.get)
    imprimir_nodos(lista)


# Tiempo igual a similares + un recorrido extra para eliminar adyacentes
def recomendar(grafo, vertice, k):
    """
    Dado un vertice, encuentra los vertices más similares a este con los cuales no tiene relación.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id de un vertice.
    :param k: Int - Cantidad de similares a buscar.
    """
    aux = n_random_walks(grafo, vertice, N_WALKS, WALKS_LARGE)
    result = {k: v for k, v in aux.items() if not grafo.son_adyacentes(k, vertice)}
    lista = heapq.nlargest(k, result, key=result.get)
    imprimir_nodos(lista)


# Tiempo O(E + V) (bfs)
def camino(grafo, vertice1, vertice2):
    """
    Busca el camino más corto para llegar desde vertice1 hasta vertice2.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice1: String - Id del vertice de partida.
    :param vertice2: String - Id del vertice de llegada.
    """
    lista = grafo.camino_minimo(vertice1, vertice2)
    if lista:
        imprimir_camino(lista)
    else:
        imprimir_error("Los vertices no se unen.")


def centralidad_exacta(grafo, n):
    """
    Busca los vertices que aparecen más veces entre todos los caminos mínimos existentes en el grafo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param n: Int - Cantidad de vertices a buscar.
    """
    _, _, apariciones = grafo.bfs()
    lista = heapq.nlargest(n, apariciones, key=apariciones.get)
    imprimir_nodos(lista)


def centralidad_aproximada(grafo, n):
    """
    Busca una aproximación de los vertices que aparecen más veces
        entre todos los caminos mínimos existentes en el grafo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param n: Int - Cantidad de vertices a buscar.
    """
    ocurrencias = {}
    for _ in range(N_RANDOM_CHOICE):
        vertices = grafo.obtener_vertices()
        v = random.choice(vertices)
        aux = n_random_walks(grafo, v, N_WALKS, WALKS_LARGE)
        for k, v in aux.items():
            if k not in ocurrencias:
                ocurrencias[k] = 1
            ocurrencias[k] += 1
    lista = heapq.nlargest(n, ocurrencias, key=ocurrencias.get)
    imprimir_nodos(lista)


def distancias(grafo, vertice):
    """
    Dado un vertice, obtiene los vertices que se encuentran a cada una de las distancias posibles,
        considerando las distancias como la cantidad de saltos.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id del vertice de partida.
    """
    _, orden, _ = grafo.bfs(vertice)

    dist = {}
    for k, v in orden.items():
        if v not in dist:
            dist[v] = []
        dist[v].append(k)

    imprimir_distancias(dist)


def estadisticas(grafo):
    """
    Obtiene algunas estadisticas del grafo:
        *Cantidad de vértices.
        *Cantidad de aristas.
        *Promedio de grado de entrada de cada vértice.
        *Promedio de grado de entrada de cada vértice.
        *Densidad del grafo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    """
    imprimir_estadisticas(grafo.cantidad_vertices(), grafo.cantidad_aristas())


def comunidades(grafo):
    """
    Busca las comunidades que se encuentren en el grafo. Utilizando el algoritmo de label propagation
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    """
    label = {}

    i = 1
    for v in grafo:
        label[v] = str(i)
        i += 1

    for _ in range(LABEL_ITER):
        recorrido = random_walk(grafo, random.choice(grafo.obtener_vertices()), LABEL_WALKS_LARGE)
        for e in recorrido:
            etiquetas_adyacentes = [label[e] for e in grafo.obtener_adyacentes(e)]
            # + random.random() -> Para que max() elija uno random en caso de empate
            # (Se suma un numero < 1 por lo que no cambia el resultado)
            label[e] = max(etiquetas_adyacentes, key=lambda x: etiquetas_adyacentes.count(x) + random.random())

    comunidad = {}
    for k, v in label.items():
        if v not in comunidad:
            comunidad[v] = []
        comunidad[v].append(k)

    for k, v in comunidad.items():
        if len(v) > 2000 or len(v) < 4:
            continue
        imprimir_comunidad(k, v)


# Realiza n random walks y devuelve un mapa con la cuenta de las veces que aprecio cada nodo
def n_random_walks(grafo, vertice, n, pasos):
    """
    Realiza n random walks y cuenta las apariciones de cada nodo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id del vertice de partida.
    :param n: Int - Cantidad de random walks a ejecutar.
    :param pasos: Int - Cantidad de pasos de cada random walk.
    :return: Map<String, Int> - las apariciones de cada nodo.
    """
    aux = {}
    for _ in range(n):
        recorrido = random_walk(grafo, vertice, pasos)
        for v in recorrido:
            if v in aux:
                aux[v] += 1
            else:
                aux[v] = 1

    if vertice in aux:
        aux.pop(vertice)
    return aux


def random_walk(grafo, vertice, pasos):
    """

    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id del vertice de partida.
    :param pasos: Int - Cantidad de pasos del random walk.
    :return: El recorrido del random walk
    """
    return __aux_random_walk(grafo, vertice, pasos, [])


def __aux_random_walk(grafo, vertice, pasos, recorrido):
    if recorrido is None:
        recorrido = []
    if pasos == 0:
        return recorrido
    l = grafo.obtener_adyacentes(vertice)
    e = random.choice(l)
    recorrido.append(e)
    return __aux_random_walk(grafo, e, pasos - 1, recorrido)


if __name__ == "__main__":
    main()
