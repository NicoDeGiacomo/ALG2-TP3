import sys
import csv
from grafo import Grafo
import random
import heapq

N_WALKS = 500
WALKS_LARGE = 100


# cat comandos.txt | python3 ./tp3.py asd.txt
def main():
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
    if command == "centralidad":
        return centralidad(grafo, args[0])
    if command == "distancias":
        return distancias(grafo, args[0])
    if command == "estadisticas":
        return estadisticas(grafo)
    if command == "comunidades":
        return comunidades(grafo)


def similares(grafo, vertice, k):
    # Tiempo: random walks (lineal) + n mayores con heap (n*log(k)) n->Cantidad de nodos total de todos los recorridos
    imprimir_comando("similares", vertice, k)
    aux = {}
    for _ in range(N_WALKS):
        recorrido = random_walk(grafo, vertice, WALKS_LARGE)
        for v in recorrido:
            if v in aux:
                aux[v] += 1
            else:
                aux[v] = 1

    aux.pop(vertice)
    l = heapq.nlargest(int(k), aux, key=aux.get)
    print(", ".join(map(str, l)), end="\n \n")


def recomendar(grafo, vertice, n):
    imprimir_comando("recomendar", vertice, vertice, n)


def camino(grafo, id1, id2):
    imprimir_comando("camino", id1, id2)


def centralidad(grafo, n):
    imprimir_comando("centralidad", n)


def distancias(grafo, vertice):
    imprimir_comando("distancias", vertice)


def estadisticas(grafo):
    imprimir_comando("estadisticas")


def comunidades(grafo):
    imprimir_comando("comunidades")


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
