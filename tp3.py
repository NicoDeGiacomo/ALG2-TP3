# coding=utf-8
"""
Alumnos: De Giacomo - Ponce
Padrones: 99702 - 99723
Corrector: Agustina Mendez
"""
import cmd
import csv
from grafo import Grafo
import random
import heapq
from salida import *

N_WALKS = 100
WALKS_LARGE = 100
N_RANDOM_CHOICE = 20
LABEL_ITER = 100
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
    """
    Recibe un comando a ejecutar y llama a la función correspondiente.
    :param command: String - Comando a ejecutar.
    :param args: List<String> - Lista de parámetros para la ejecución del comando.
    :param grafo: Grafo - Grafo sobre el cual ejecutar el comando.
    """
    command = str(command).rstrip()
    if command == "similares":
        if len(args) != 2:
            imprimir_error("-similares requiere 2 parametros-")
            return
        imprimir_comando("similares", str(args[0]).rstrip(), int(args[1]))
        lista = similares(grafo, str(args[0]).rstrip(), int(args[1]))
        imprimir_nodos(lista)
        return

    if command == "recomendar":
        if len(args) != 2:
            imprimir_error("-recomendar requiere 2 parametros-")
            return
        imprimir_comando("recomendar", str(args[0]).rstrip(), int(args[1]))
        lista = recomendar(grafo, str(args[0]).rstrip(), int(args[1]))
        imprimir_nodos(lista)
        return

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
        return

    if command == "centralidad_exacta":
        if len(args) != 1:
            imprimir_error("-centralidad_exacta requiere 1 parametro-")
            return
        imprimir_comando("centralidad_exacta", int(args[0]))
        lista = centralidad_exacta(grafo, int(args[0]))
        imprimir_nodos(lista)
        return

    if command == "centralidad_aproximada":
        if len(args) != 1:
            imprimir_error("-centralidad_aproximada requiere 1 parametro-")
            return
        imprimir_comando("centralidad_aproximada", int(args[0]))
        lista = centralidad_aproximada(grafo, int(args[0]))
        imprimir_nodos(lista)
        return

    if command == "distancias":
        if len(args) != 1:
            imprimir_error("-distancias requiere 1 parametro-")
            return
        imprimir_comando("distancias", str(args[0]).rstrip())
        dist = distancias(grafo, str(args[0]).rstrip())
        imprimir_distancias(dist)
        return

    if command == "estadisticas":
        if len(args) != 0:
            imprimir_error("-estadisticas no requiere parametros-")
            return
        imprimir_comando("estadisticas")
        vertices, aristas = estadisticas(grafo)
        imprimir_estadisticas(vertices, aristas)
        return

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
        return

    imprimir_error("El comando indicado no fue reconocido: " + str(command))


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


def centralidad_exacta(grafo, k):
    """
    Busca los vertices que aparecen más veces entre todos los caminos mínimos existentes en el grafo.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param k: Int - Cantidad de vertices a buscar.
    :return: List - Lista con los ids de los n vertices mas centrales.
    """
    _, _, apariciones = grafo.bfs()
    lista = heapq.nlargest(k, apariciones, key=apariciones.get)
    return lista


def centralidad_aproximada(grafo, k):
    """
    Busca una aproximación de los vertices mas centrales.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :param k: Int - Cantidad de vertices a buscar.
    :return: List - Lista con los ids de los n vertices mas centrales.
    """
    aux = {}
    for _ in range(N_RANDOM_CHOICE):
        aux = n_random_walks(grafo, grafo.vertice_aleatorio(), N_WALKS, WALKS_LARGE)
    lista = heapq.nlargest(k, aux, key=aux.get)
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

    # Invierto el diccionario para obtener los vertices a cada distancia
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
    Busca las comunidades que se encuentren en el grafo, utilizando el algoritmo de label propagation.
    :param grafo: Grafo - Grafo sobre el cual ejecutar la función.
    :return: Map<String, List<String>> - Mapa con una lista de ids de vertices para cada label de una comunidad
    """
    label = {}

    i = 1
    for v in grafo:
        label[v] = str(i)
        i += 1

    for _ in range(LABEL_ITER):
        # Establezco un recorrido random para cada iteración, empezando en un vertice random.
        recorrido = grafo.random_walk(LABEL_WALKS_LARGE)
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
        recorrido = grafo.random_walk(pasos, vertice)
        for v in recorrido:
            if v in aux:
                aux[v] += 1
            else:
                aux[v] = 1

    if vertice in aux:
        aux.pop(vertice)
    return aux


class GraphAnalysisShell(cmd.Cmd):
    intro = 'Welcome to the graph analysis shell.   Type \'help\' or \'?\' to list commands.\n'
    prompt = '(Graph Analysis)'

    def do_similares(self, args):
        """Encuentra los vertices mas similares: similares 1"""
        do_function("similares", args, grafo)



if __name__ == "__main__":
    main()
