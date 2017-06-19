import sys
import csv
from grafo import Grafo
import random
import heapq
from collections import deque

N_WALKS = 500
WALKS_LARGE = 100


# cat comandos.txt | python3 ./tp3.py asd.txt
def main():
    # TODO: SACAR ESTA BAZOFIA
    sys.stdin = open('comandos.txt', 'r')

    if len(sys.argv) != 2:
        print("-Please provide 1 arguments-", file=sys.stderr)
        print("-Usage: tp3.py <inputfile>", file=sys.stderr)
        sys.exit(2)

    grafo = Grafo()

    print("\nLoading file ...\n")
    with open(sys.argv[1], "r") as file:
        for _ in range(4):
            next(file)
        reader = csv.DictReader(file, delimiter="\t", fieldnames=["a", "b"])
        for line in reader:
            grafo.agregar_vertice(line["a"])
            grafo.agregar_vertice(line["b"])
            grafo.agregar_arista(line["a"], line["b"])

    # Leo por entrada standard
    print("Reading commands ...\n")
    for line in sys.stdin:
        comando = line.split(" ")
        do_function(comando[0], comando[1:], grafo)


def do_function(command, args, grafo):
    # TODO: Hay que checkear los parametros ?

    if command == "similares":
        return similares(grafo, args[0], args[1])
    if command == "recomendar":
        return recomendar(grafo, args[0], args[1])
    if command == "camino":
        return camino(grafo, args[0], args[1])
    if command == "centralidad_exacta":
        return centralidad_exacta(grafo, args[0])
    if command == "centralidad_aproximada":
        return centralidad_aproximada(grafo, args[0])
    if command == "distancias":
        return distancias(grafo, args[0])
    if command == "estadisticas":
        return estadisticas(grafo)
    if command == "comunidades":
        return comunidades(grafo)


def similares(grafo, vertice, k):
    # Tiempo: random walks (lineal) + n mayores con heap (n*log(k)) n->Cantidad de nodos total de todos los recorridos
    imprimir_comando("similares", vertice, k)
    aux = n_random_walks(grafo, vertice, k)
    l = heapq.nlargest(int(k), aux, key=aux.get)
    # TODO: funcion para imprimir resultados (Tambien otra para imprimir errores?)
    print(", ".join(map(str, l)), end="\n \n")


def recomendar(grafo, vertice, k):
    # Tiempo igual a similares + un recorrido extra para eliminar adyacentes
    imprimir_comando("recomendar", vertice, k)
    aux = n_random_walks(grafo, vertice, k)
    new_data = {k: v for k, v in aux.items() if not grafo.son_adyacentes(k, vertice)}
    l = heapq.nlargest(int(k), new_data, key=new_data.get)
    print(", ".join(map(str, l)), end="\n \n")


# TODO: SACAR TODOS LOS \N A LOS PARAMETROS
# TODO: CASO DE QUE NO TRAIGA NADA BFS (NO SE CONECTAN) -> CHECKEAR QUE EXISTAN AMBOS ANTES AL MENOS ? Y QUE ESTEN CONECTADOS?
def camino(grafo, id1, id2):
    # Tiempo O(E + V) (bfs)
    imprimir_comando("camino", id1, id2)
    l = bfs(grafo, id1, str(int(id2)))
    if not l:
        print("No path", end="\n \n")
    else:
        print(" -> ".join(map(str, l)), end="\n \n")


def centralidad_exacta(grafo, n):
    imprimir_comando("centralidad_exacta", n)
    # Tiempo O( V*(E + V) ) (bfs por cada vertice)
    ocurrencias = {}
    count = 0
    ocurrencias = all_bfs(grafo)
    l = heapq.nlargest(int(n), ocurrencias, key=ocurrencias.get)
    if not l:
        print("No path")
    else:
        print(", ".join(map(str, l)), end="\n \n")


def centralidad_aproximada(grafo, n):
    imprimir_comando("centralidad_aproximada", n)


def distancias(grafo, vertice):
    imprimir_comando("distancias", vertice)


def estadisticas(grafo):
    imprimir_comando("estadisticas")


def comunidades(grafo):
    imprimir_comando("comunidades")


def n_random_walks(grafo, vertice, k):
    aux = {}
    for _ in range(N_WALKS):
        recorrido = random_walk(grafo, vertice, WALKS_LARGE)
        for v in recorrido:
            if v in aux:
                aux[v] += 1
            else:
                aux[v] = 1

    aux.pop(vertice)
    return aux


# TODO: Poner esto en español y mas lindo
# Recibe end -> Camino mas corto de start a end
# No recibe end -> Camino mas corto de start a todos los nodos
def bfs(graph_to_search, start, end):
    queue = deque([start])
    visited = set()
    while queue:
        # Gets the first path in the queue
        path = queue.popleft()
        # Gets the last node in the path
        vertex = path[-1]
        # Checks if we got to the end
        if vertex == end:
            return path
        # We check if the current node is already in the visited nodes set in order not to recheck it
        elif vertex not in visited:
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            for current_neighbour in graph_to_search.obtener_adyacentes(vertex):
                new_path = list(path)
                new_path.append(current_neighbour)
                queue.append(new_path)
            # Mark the vertex as visited
            visited.add(vertex)


def all_bfs(graph_to_search):
    paths = {}
    for v in graph_to_search:
        done = {}
        queue = deque([v])
        visited = set()
        while queue:
            # Gets the first path in the queue
            path = queue.popleft()
            # Gets the last node in the path
            vertex = path[-1]
            # Checks if we got to the end
            if vertex not in done:
                done[vertex] = True
                for e in path:
                    if e in paths:
                        paths[e] += 1
                    else:
                        paths[e] = 1
            # We check if the current node is already in the visited nodes set in order not to recheck it
            if vertex not in visited:
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                for current_neighbour in graph_to_search.obtener_adyacentes(vertex):
                    new_path = list(path)
                    new_path.append(current_neighbour)
                    queue.append(new_path)
                # Mark the vertex as visited
                visited.add(vertex)
    return paths


def random_walk(grafo, id, pasos, recorrido=None):
    if recorrido is None:
        recorrido = []
    if pasos == 0:
        return recorrido
    l = grafo.obtener_adyacentes(id)
    e = random.choice(l)
    recorrido.append(e)
    return random_walk(grafo, e, pasos - 1, recorrido)


def imprimir_comando(command, *args):
    print(command, end=" ")
    print(" ".join(map(str, args)), end="")


if __name__ == "__main__":
    main()
