# coding=utf-8
"""
Alumnos: De Giacomo - Ponce
Padrones: 99702 - 99723
Corrector: Agustina Mendez
"""
from collections import deque


class Grafo:
    """
    TDA grafo. Implementado como diccionario de diccionarios.
    """

    def __init__(self, bidireccional=True):
        self.bidireccional = bidireccional
        self.dict = {}
        self.n_aristas = 0

    def agregar_vertice(self, vertice):
        """
        Agrega un vertice al grafo.
        :param vertice: String - Id del vertice a insertar.
        :return: True si se agrego correctamente. False en caso contrario.
        """
        if vertice in self.dict:
            return False
        self.dict[vertice] = {}
        return True

    def agregar_arista(self, vertice1, vertice2, peso=1):
        """
        Agrega una arista al grafo.
        :param vertice1: String - Id del vertice de salida.
        :param vertice2: String - Id del vertice de entrada.
        :param peso: Int - Peso de la arista.
        :return: True si se agrego correctamente. False en caso contrario.
        """
        if not self._existen_vertices([vertice1, vertice2]):
            return False
        self.dict[vertice1][vertice2] = peso
        if self.bidireccional:
            self.dict[vertice2][vertice1] = peso
        else:
            self.dict[vertice2][vertice1] = -peso
        self.n_aristas += 1
        return True

    def eliminar_arista(self, vertice1, vertice2):
        """
        Elimina una arista.
        :param vertice1: String - Id del vertice de salida.
        :param vertice2: String - Id del vertice de entrada.
        :return: True si se elimino correctamente. False en caso contrario.
        """
        if not self._existen_vertices([vertice1, vertice2]):
            return False
        self.dict[vertice1].pop(vertice2)
        if self.bidireccional:
            self.dict[vertice2].pop(vertice1)
        self.n_aristas -= 1
        return True

    def son_adyacentes(self, vertice1, vertice2):
        """
        Devuelve si dos vertices son adyacentes.
        :param vertice1: String - Id del vertice de salida.
        :param vertice2: String - Id del vertice de entrada.
        :return: True si son adyacentes. False en caso contrario.
        """
        if not self._existen_vertices([vertice1, vertice2]):
            return False
        return vertice2 in self.dict[vertice1]

    def obtener_adyacentes(self, vertice):
        """
        Obtiene los adyacentes de un vertice.
        :param vertice: String - Id de un vertice.
        :return: List<String> - Lista de los ids de los vertices adyacentes.
        """
        if not self.existe_vertice(vertice):
            return []
        return list(self.dict.get(vertice).keys())

    def existe_vertice(self, vertice):
        """
        Devuelve si un vertice existe.
        :param vertice: String - Id de un vertice.
        :return: True en caso afirmativo. False en caso contrario.
        """
        return vertice in self.dict

    def obtener_vertices(self):
        """
        Obtiene todos los vertices del grafo.
        :return: List<String> - Lista con los ids de todos los vertices.
        """
        return list(self.dict.keys())

    def cantidad_vertices(self):
        """
        Devuelve la cantidad de vertices en el grafo.
        :return: Int - Cantidad de vertices en el grafo.
        """
        return len(self.obtener_vertices())

    def cantidad_aristas(self):
        """
        Devuelve la cantidad de aristas en el grafo.
        :return: Int - Cantidad de aristas en el grafo.
        :return:
        """
        return self.n_aristas

    def __iter__(self):
        return iter(self.dict)

    def _existen_vertices(self, vertices):
        for v in vertices:
            if not self.existe_vertice(v):
                return False
        return True

    def camino_minimo(self, v, w):
        """
        Realiza una busqueda de camino minimo para v -> ... -> w.
        :param v: Id del vertice de salida.
        :param w: Id del vertice de llegada.
        :return: List<String> - Lista de ids del los vertices del recorrido.
        """
        visitados = {}
        padre = {v: None}
        orden = {v: 0}
        self._bfs_visitar(v, visitados, padre, orden, w)
        if w not in visitados:
            return None
        # Backtrace
        camino = [w]
        while camino[-1] != v:
            camino.append(padre[camino[-1]])
        camino.reverse()
        return camino

    def bfs(self, v=None):
        """
        Realiza un recorrido BFS sobre el grafo para todos los vertices (A menos que reciba un vertices específico)
        :param v: Id del vertice de partida -> default: Se realiza BFS sobre todos los vertices
        :return:    * Map<String, String> - Un diccionario con los padres de cada vertice
                    * Map<String, Int> - Un diccionario con el orden de cada vertice
                    * Map<String, Int> - Un diccionario con las apariciones de cada vertice
        """
        apariciones = {}
        padre = {}
        orden = {}
        if v:
            padre = {v: None}
            orden = {v: 0}
            self._bfs_visitar(v, apariciones, padre, orden)
        else:
            for v in self:
                if v not in apariciones:
                    padre[v] = None
                    orden[v] = 0
                    self._bfs_visitar(v, apariciones, padre, orden)
        return padre, orden, apariciones

    def _bfs_visitar(self, origen, visitados, padre, orden, y=None):
        q = deque()
        q.append(origen)
        visitados[origen] = 1
        while len(q) > 0:
            v = q.popleft()
            for w in self.obtener_adyacentes(v):
                if w not in visitados:
                    visitados[w] = 1
                    padre[w] = v
                    orden[w] = orden[v] + 1
                    q.append(w)
                    if w == y:
                        return
                else:
                    visitados[w] += 1
