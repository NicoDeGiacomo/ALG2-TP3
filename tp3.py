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


# cat comandos.txt | python3 ./tp3.py asd.txt
def main():
    # TODO: SACAR ESTA BAZOFIA
    sys.stdin = open('comandos.txt')

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
    # toto imprimir la salida tambien en esta funcion
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
    aux = n_random_walks(grafo, vertice, N_WALKS, WALKS_LARGE)
    lista = heapq.nlargest(k, aux, key=aux.get)
    imprimir_nodos(lista)


# Tiempo igual a similares + un recorrido extra para eliminar adyacentes
def recomendar(grafo, vertice, k):
    aux = n_random_walks(grafo, vertice, N_WALKS, WALKS_LARGE)
    result = {k: v for k, v in aux.items() if not grafo.son_adyacentes(k, vertice)}
    lista = heapq.nlargest(k, result, key=result.get)
    imprimir_nodos(lista)


# Tiempo O(E + V) (bfs)
def camino(grafo, vertice1, vertice2):
    lista = grafo.camino_minimo(vertice1, vertice2)
    if lista:
        imprimir_camino(lista)
    else:
        imprimir_error("Los vertices no se unen.")


def centralidad_exacta(grafo, n):
    _, _, apariciones = grafo.bfs()
    lista = heapq.nlargest(n, apariciones, key=apariciones.get)
    imprimir_nodos(lista)


def centralidad_aproximada(grafo, n):
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
    _, orden, _ = grafo.bfs(vertice)

    dist = {}
    for k, v in orden.items():
        if v not in dist:
            dist[v] = []
        dist[v].append(k)

    imprimir_distancias(dist)


def estadisticas(grafo):
    imprimir_estadisticas(grafo.cantidad_vertices(), grafo.cantidad_aristas())


def comunidades(grafo):
    label = {}

    i = 1
    for v in grafo:
        label[v] = str(i)
        i += 1

    for _ in range(LABEL_ITER):
        recorrido = []
        random_walk(grafo, random.choice(grafo.obtener_vertices()), LABEL_WALKS_LARGE, recorrido)
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
        print("Comunidad " + k + ": Integrantes: " + str(len(v)) + "--> " + str(v))


# Realiza n random walks y devuelve un mapa con la cuenta de las veces que aprecio cada nodo
def n_random_walks(grafo, vertice, n, pasos):
    aux = {}
    for _ in range(n):
        recorrido = random_walk(grafo, vertice, pasos)
        for v in recorrido:
            if v in aux:
                aux[v] += 1
            else:
                aux[v] = 1

    return aux


def random_walk(grafo, id, pasos, recorrido=None):
    if recorrido is None:
        recorrido = []
    if pasos == 0:
        return recorrido
    l = grafo.obtener_adyacentes(id)
    e = random.choice(l)
    recorrido.append(e)
    return random_walk(grafo, e, pasos - 1, recorrido)


if __name__ == "__main__":
    main()
