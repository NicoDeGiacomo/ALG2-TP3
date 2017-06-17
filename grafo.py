class Grafo:
    def __init__(self):
        self.dict = {}

    def agregar_vertice(self, vertice):
        if vertice in self.dict:
            return False
        self.dict[vertice] = {}
        return True

    def agregar_arista(self, vertice1, vertice2, peso=1, bidireccional=True):
        if not self.__existen_vertices__([vertice1, vertice2]):
            return False
        self.dict[vertice1][vertice2] = peso
        if bidireccional:
            self.dict[vertice2][vertice1] = peso
        return True

    def eliminar_arista(self, vertice1, vertice2):
        if not self.__existen_vertices__([vertice1, vertice2]):
            return False
        self.dict[vertice1].pop(vertice2)
        self.dict[vertice2].pop(vertice1)
        return True

    def son_adyacentes(self, vertice1, vertice2):
        if not self.__existen_vertices__([vertice1, vertice2]):
            return False
        return vertice2 in self.dict[vertice1]

    def obtener_adyacentes(self, vertice):
        return self.dict.get(vertice)

    def existe_vertice(self, vertice):
        return vertice in self.dict

    def obtener_vertices(self):
        return list(self.dict.keys())

    def cantidad_vertices(self):
        return len(self.obtener_vertices())

    def __iter__(self):
        return iter(self.dict)

    def __existen_vertices__(self, vertices):
        for v in vertices:
            if v not in self.dict:
                return False
        return True
