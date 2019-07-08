from collections import deque as Deque

class Grafo(object):
    def __init__(self):
        self.vertices = {}
        self.cantidad_vertices = 0
        self.cantidad_artistas = 0

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices: 
            self.cantidad_vertices += 1
            self.vertices[vertice] = set()

    def eliminar_vertice(self, vertice):
        if vertice in self.vertices:
            for adyacente in self.vertices[vertice]:
                self.vertices[vertice].remove(adyacente)
                self.cantidad_artistas -= 1
            self.vertices.pop(vertice)
            self.cantidad_vertices -= 1

    def devolver_cantidad_vertices(self):
        return self.cantidad_vertices

    def existe_vertice(self, vertice):
        return vertice in self.vertices
        
    def devolver_valor_vertice(self, vertice):
        if vertice in self.vertices: return self.vertices[vertice]

    def agregar_arista(self, origen, destino):
        if origen in self.vertices:
            self.vertices[origen].add(destino)
            self.cantidad_artistas += 1

    def eliminar_arista(self, origen, destino):
        if origen in self.vertices:
            self.vertices[origen].remove(destino)
            self.cantidad_artistas -= 1

    def devolver_cantidad_artistas(self):
        return self.cantidad_artistas

    def existe_arista(self, origen, destino):
        if origen in self.vertices: return destino in self.vertices[origen]

    def bfs(self, origen, funcion = None):
        padres = {}
        orden = {}
        visitados = set() 
        cola = Deque()
        padres[origen] = None
        orden[origen] = 0
        cola.append(origen)
        while len(cola) != 0:
            actual = cola.popleft()
            if funcion: funcion(actual)
            for adyacente in self.vertices[actual]:
                if adyacente not in visitados:
                    visitados.add(actual)
                    padres[adyacente] = actual
                    orden[adyacente] = orden[actual] + 1
                    cola.append(adyacente)
        return padres,orden

    def reconstruir_ciclo(padre, inicio, fin):
        v = fin
        camino = []
        while v != inicio:
            camino.append(v)
            v = padre[v]
        camino.append(inicio)
        return camino.invertir()        
        
    def bfs_ciclo(self, v, visitados):
        q = Cola()
        q.encolar(v)
        visitados[v] = True
        padre = {} 
        padre[v] = None

        while not q.esta_vacia():
            v = q.desencolar()
            for w in self.vertices.adyacentes(v):
                if w in visitados:
                    if w != padre[v]:
                        return reconstruir_ciclo(padre, w, v)
                else:
                    q.encolar(w)
                    visitados[v] = True
                    padre[w] = v

        return None

    def obtener_ciclo_bfs(self):
        visitados = {}
        for v in self.vertices:
            if v not in visitados:
                ciclo = bfs_ciclo(self.vertices, v, visitados)
            if ciclo is not None:
                return ciclo
        return None


    def dfs(self, origen, funcion = None):
        visitados = set()
        pila = Deque()
        _dfs(self, origen, pila, visitados, funcion)

    def _dfs(self, actual, pila, visitados, funcion = None):
        if funcion: function(actual)
        visitados.add(actual)
        for adyacente in self.vertices[actual]:
            if adyacente not in visitados: _dfs(self, adyacente, funcion, pila, visitados)
        pila.append(adyacente)

    def orden_topologico(self):
        grados = {}
        resultado = []
        cola = Deque()
        for vertice in self.vertices: grados[vertice] = 0
        for vertice in self.vertices:
            for adyacente in vertice:
                grados[adyacente] += 1
        for vertice in self.vertices:
            if grados[vertice] == 0: cola.add(vertice)
        while maxlen(cola):
            actual = cola.popleft()
            resultado.append(actual)
            for adyacente in actual:
                grados[adyacente] -= 1
                if grados[adyacente] == 0: cola.add(adyacente)
        if len(resultado) == len(grafo):
            return resultado 
        return None #tiene ciclo

        
    