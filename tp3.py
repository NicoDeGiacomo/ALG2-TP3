import sys
import csv
from grafo import Grafo


def main():
    if len(sys.argv) != 2:
        print("-Please provide 1 arguments-", file=sys.stderr)
        print("-Usage: tp3.py <inputfile>", file=sys.stderr)
        sys.exit(2)

    grafo = Grafo()

    print("Loading file ...")
    with open(sys.argv[1], "r") as file:
        for _ in range(4):
            next(file)
        reader = csv.DictReader(file, delimiter="\t", fieldnames=["a","b"])
        for line in reader:
            grafo.agregar_vertice(line["a"])
            grafo.agregar_vertice(line["b"])
            grafo.agregar_arista(line["a"], line["b"])

    # Leo por entrada standard
    print("Reading commands ...")
    for line in sys.stdin:
        print(line)
        comando = line.split(" ")
        do_function(comando[0], comando[1:], grafo)


def do_function(command, args, grafo):
    # TODO: Hay que checkear los parametros ?

    if command == "similares":
        return similares(args[0], args[1], grafo)
    if command == "recomendar":
        return recomendar(args[0], args[1], grafo)
    if command == "camino":
        return camino(args[0], args[1], grafo)
    if command == "centralidad":
        return centralidad(args[0], grafo)
    if command == "distancia":
        return distancia(args[0], grafo)
    if command == "estadisticas":
        return estadisticas(grafo)
    if command == "comunidades":
        return comunidades(grafo)


def similares(id, n, grafo):
    print("Entro a func similares")


def recomendar(id, n, grafo):
    print("Entro a func recomendar")


def camino(id1, id2, grafo):
    print("Entro a func (")


def centralidad(n, grafo):
    print("Entro a func centralidad")


def distancia(id, grafo):
    print("Entro a func distancia")


def estadisticas(grafo):
    print("Entro a func estadisticas")


def comunidades(grafo):
    print("Entro a func comunidades")


if __name__ == "__main__":
    main()
