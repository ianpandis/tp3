from collections import deque as Deque

class Grafo(object):
    def __init__(self):
        self.vertices = {}
        self.cantidad_vertices = 0
        self.cantidad_artistas = 0

    def adyacentes(self, clave):
        return list(self.vertices.get(clave, None))

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices: 
            self.cantidad_vertices += 1
            self.vertices[vertice] = {}

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
            valores = self.vertices.get(origen, {})
            valores[destino] = None #no tiene pesos
            self.vertices[origen] = valores
            self.cantidad_artistas += 1

    def eliminar_arista(self, origen, destino):
        if origen in self.vertices:
            self.vertices[origen].remove(destino)
            self.cantidad_artistas -= 1

    def devolver_cantidad_artistas(self):
        return self.cantidad_artistas

    def existe_arista(self, origen, destino):
        if origen in self.vertices: return destino in self.vertices[origen]

    def bfs(self, vertice_inicial):
        visitados = set()
        distancia = {}
        padres = {}
        q = Deque()
        q.append(vertice_inicial)
        padres[vertice_inicial] = None
        visitados.add(vertice_inicial)
        distancia[vertice_inicial] = 0

        while(len(q) > 0):
            v = q.popleft()
            for w in grafo.adyacentes(v):
                if w not in visitados:
                    visitados.add(w)
                    distancia[w] = distancia[v] + 1
                    padres[w] = v
                    q.append(w)
        return distancia, padres

    def obtener_ciclo_dfs(self, inicio):
        visitados = {}
        padres = {}
        ciclos = []
        ciclo = self.dfs_ciclo(inicio, visitados, padres, ciclos)
        return ciclos

    def dfs_ciclo(self, v, visitados, padres, ciclos): 
        visitados[v] = True
        for w in self.adyacentes(v):
            if w in visitados:
                if w != padres[v]:
                    ciclos.append(self.reconstruir_ciclo(padres, w, v))
            else:
                padres[w] = v
                ciclo = self.dfs_ciclo(w, visitados, padres, ciclos)
                if ciclo is not None:
                    return ciclo
        return ciclos

    def reconstruir_ciclo(self, padres, inicio, fin):
        v = fin
        camino = []
        while v != inicio:
            camino.insert(0, v)
            v = padres[v]
        camino.insert(0, inicio)
        return camino  

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

        
    