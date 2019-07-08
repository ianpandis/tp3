import csv
from Grafo import Grafo
import sys

def main():
    if len(sys.argv) != 2:
        print("Error: Cantidad de parametros incorrectos. Intente nuevamente.") 
        return
    archivo = cargar_grafo(sys.argv[1])
    cfc(archivo)
    #divulgar_ciclo(archivo, 63, 1) #falta este tambien
    #divulgar(archivo, 1, 7)
    #min_seguimientos(archivo, 1, 7)
    
def cargar_grafo(nombre_archivo):
    with open(nombre_archivo) as delincuentes:
        delincuentes_tsv = csv.reader(delincuentes, delimiter="\t")
        grafo = Grafo()
        for linea in delincuentes_tsv:
            if not grafo.existe_vertice(int(linea[0])):
                grafo.agregar_vertice(int(linea[0]))
            if not grafo.existe_vertice(int(linea[1])):
                grafo.agregar_vertice(int(linea[1]))
            grafo.agregar_arista(int(linea[0]), int(linea[1]))                
    return grafo

def min_seguimientos(grafo, origen, destino):
    resultado = []
    cadena = ""
    padres,orden = grafo.bfs(origen, None)
    if destino not in padres:
        print("Seguimiento Imposible")
        return
    resultado.insert(0, destino)
    padre = padres[destino]
    while padre != None:
        resultado.insert(0, padre)
        padre = padres[padre]
    largo_resultado = len(resultado)
    for indice in range(largo_resultado):
        cadena += str(resultado[indice])
        if indice + 1 != largo_resultado: cadena += " -> "
    print(cadena)

def divulgar(grafo, delincuente, n):
    padres,orden = grafo.bfs(delincuente, None)
    resultado = ""
    for clave in orden:
        if orden[clave] < n: resultado += str(clave) + ", "
        else: break
    resultado = resultado[:-2]
    print(resultado)

def divulgar_ciclo(grafo, delincuente, n):
    resultado = grafo.obtener_ciclo_bfs()
    print(resultado)

def dfs_cfc(vertices, vertice, visitados, orden, lista1, lista2, cfcs, en_cfs):
    visitados.add(vertice)
    lista1.append(vertice)
    lista2.append(vertice)
    for adyacente in vertices[vertice]:
        if adyacente not in visitados:
            orden[adyacente] = orden[vertice] + 1
            dfs_cfc(vertices, adyacente, visitados, orden, lista1, lista2, cfcs, en_cfs)
        elif adyacente not in en_cfs:
            while orden[lista1[-1]] > orden[adyacente]:
                lista1.pop()

    if lista1.ver_tope() == vertice:
        lista1.pop()
        aux = None
        nueva_cfc = []
        while aux != vertice:
            aux = lista2.pop()
            en_cfs.add(aux)
            nueva_cfc.append(aux)
        cfcs.add(nueva_cfc)

def cfc(grafo):
	visitados = set()
	orden = {}
	lista1 = []
	lista2 = []
	cfcs = []
	en_cfs = set()
	for vertice in grafo.vertices:
		if vertice not in visitados:
			orden[vertice] = 0
			dfs_cfc(grafo.vertices, vertice, visitados, orden, lista1, lista2, cfcs, en_cfs)
	return cfcs

main()