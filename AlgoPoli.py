import csv
from Grafo import Grafo
import sys

def main():
    if len(sys.argv) != 2:
        print("Error: Cantidad de parametros incorrectos. Intente nuevamente.") 
        return
    archivo = cargar_grafo(sys.argv[1])

def cargar_grafo(nombre_archivo):
    with open(nombre_archivo) as delincuentes:
        delincuentes_tsv = csv.reader(delincuentes, delimiter="\t")
        grafo = Grafo()
        for linea in delincuentes_tsv:
            print(grafo)
            if not grafo.existe_vertice(grafo, int(linea[0])):
                grafo.agregar_vertice(linea[0])
            if not grafo.existe_vertice(grafo, int(linea[1])):
                grafo.agregar_vertice(linea[1])
            grafo.agregar_arista(linea[0], linea[1])                
    return grafo

def min_seguimientos(origen, destino):
    resultado = []
    padres = grafo.bfs(grafo, origen, None)
    if destino not in padres:
        print("Seguimiento Imposible")
        return
    resultado.append(destino)
    padre = padres[destino]
    while padres:
        resultado.append(padre)
        padre = padres[padre]
    largo_resultado = len(resultado)
    for indice in range(largo_resultado):
        print(resultado[indice])
        if indice + 1 != largo_resultado: print("->")
main()