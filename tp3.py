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
        if len(args) != 2:
            imprimir_error("-similares requiere 2 parametros-")
            return
        imprimir_comando("similares", str(args[0]).rstrip(), int(args[1]))
        lista = similares(grafo, str(args[0]).rstrip(), int(args[1]))
        imprimir_nodos(lista)

    if command == "recomendar":
        if len(args) != 2:
            imprimir_error("-recomendar requiere 2 parametros-")
            return
        imprimir_comando("recomendar", str(args[0]).rstrip(), int(args[1]))
        lista = recomendar(grafo, str(args[0]).rstrip(), int(args[1]))
        imprimir_nodos(lista)

    if command == "camino":
        if len(args) != 2:
            imprimir_error("-camino requiere 2 parametros-")
            return
        imprimir_comando("camino", str(args[0]).rstrip(), str(args[1]).rstrip())
        lista = camino(grafo, str(args[0]).rstrip(), str(args[1]).rstrip())
        if lista:
            imprimir_camino(lista)
        else:
            imprimir_error("Los vertices no se unen.")

    if command == "centralidad_exacta":
        if len(args) != 1:
            imprimir_error("-centralidad_exacta requiere 1 parametro-")
            return
        imprimir_comando("centralidad_exacta", int(args[0]))
        lista = centralidad_exacta(grafo, int(args[0]))
        imprimir_nodos(lista)

    if command == "centralidad_aproximada":
        if len(args) != 1:
            imprimir_error("-centralidad_aproximada requiere 1 parametro-")
            return
        imprimir_comando("centralidad_aproximada", int(args[0]))
        lista = centralidad_aproximada(grafo, int(args[0]))
        imprimir_nodos(lista)

    if command == "distancias":
        if len(args) != 1:
            imprimir_error("-distancias requiere 1 parametro-")
            return
        imprimir_comando("distancias", str(args[0]).rstrip())
        dist = distancias(grafo, str(args[0]).rstrip())
        imprimir_distancias(dist)

    if command == "estadisticas":
        if len(args) != 0:
            imprimir_error("-estadisticas no requiere parametros-")
            return
        imprimir_comando("estadisticas")
        vertices, aristas = estadisticas(grafo)
        imprimir_estadisticas(vertices, aristas)

    if command == "comunidades":
        if len(args) != 0:
            imprimir_error("-comunidades no requiere parametros-")
            return
        imprimir_comando("comunidades")
        comunidad = comunidades(grafo)
        for k, v in comunidad.items():
            if len(v) > 2000 or len(v) < 4:
                continue
            imprimir_comunidad(k, v)


# Tiempo: random walks (lineal) + n mayores con heap (n*log(k)) n->Cantidad de nodos total de todos los recorridos
def similares(grafo, vertice, k):
    """
    Dado un vertice, encuentra los vertices más similares a este.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id de un vertice.
    :param k: Int - Cantidad de similares a buscar.
    :return: List - Lista con los ids de los vertices similares.
    """
    aux = n_random_walks(grafo, vertice, N_WALKS, WALKS_LARGE)
    lista = heapq.nlargest(k, aux, key=aux.get)
    return lista


# Tiempo igual a similares + un recorrido extra para eliminar adyacentes
def recomendar(grafo, vertice, k):
    """
    Dado un vertice, encuentra los vertices más similares a este con los cuales no tiene relación.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id de un vertice.
    :param k: Int - Cantidad de similares a buscar.
    :return: List - Lista con los ids de los vertices recomendados.
    """
    aux = n_random_walks(grafo, vertice, N_WALKS, WALKS_LARGE)
    result = {k: v for k, v in aux.items() if not grafo.son_adyacentes(k, vertice)}
    lista = heapq.nlargest(k, result, key=result.get)
    return lista


# Tiempo O(E + V) (bfs)
def camino(grafo, vertice1, vertice2):
    """
    Busca el camino más corto para llegar desde vertice1 hasta vertice2.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice1: String - Id del vertice de partida.
    :param vertice2: String - Id del vertice de llegada.
    :return: List - Lista con los ids de los vertices que forman el camino minimo.
                    Lista vacía en caso de que no se conecten los vértices
    """
    lista = grafo.camino_minimo(vertice1, vertice2)
    return lista


def centralidad_exacta(grafo, n):
    """
    Busca los vertices que aparecen más veces entre todos los caminos mínimos existentes en el grafo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param n: Int - Cantidad de vertices a buscar.
    :return: List - Lista con los ids de los n vertices mas centrales.
    """
    _, _, apariciones = grafo.bfs()
    lista = heapq.nlargest(n, apariciones, key=apariciones.get)
    return lista


def centralidad_aproximada(grafo, n):
    """
    Busca una aproximación de los vertices que aparecen más veces
        entre todos los caminos mínimos existentes en el grafo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param n: Int - Cantidad de vertices a buscar.
    :return: List - Lista con los ids de los n vertices mas centrales.
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
    return lista


def distancias(grafo, vertice):
    """
    Dado un vertice, obtiene los vertices que se encuentran a cada una de las distancias posibles,
        considerando las distancias como la cantidad de saltos.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param vertice: String - Id del vertice de partida.
    :return: Map<Int, String> - Mapa con una lista de ids de vertices para cada distancia.
    """
    _, orden, _ = grafo.bfs(vertice)

    dist = {}
    for k, v in orden.items():
        if v not in dist:
            dist[v] = []
        dist[v].append(k)

    return dist


def estadisticas(grafo):
    """
    Obtiene algunas estadisticas del grafo:
        *Cantidad de vértices.
        *Cantidad de aristas.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :return: (Int, Int) - Cantidad de vertices, Cantidad de aristas
    """
    return grafo.cantidad_vertices(), grafo.cantidad_aristas()


def comunidades(grafo):
    """
    Busca las comunidades que se encuentren en el grafo. Utilizando el algoritmo de label propagation
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :return: Map<String, List<String>> - Mapa con una lista de ids de vertices para cada label de una comunidad
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

    return comunidad


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
