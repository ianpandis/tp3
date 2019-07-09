import csv
from Grafo import Grafo
import sys
import random
import collections
import operator
CANT_ITERACIONES_COMUNIDADES = 20

def main():
    archivo = cargar_grafo(sys.argv[1])
    mas_imp(archivo, 3)
    #cfc(archivo)
    #divulgar(archivo, 30, 4)
    #min_seguimientos(archivo, 30, 12)
    
#FUNDIONA OK
def cargar_grafo(nombre_archivo):
    grafo = Grafo()
    with open(nombre_archivo) as delincuentes:
        delincuentes_tsv = csv.reader(delincuentes, delimiter="\t")
        for linea in delincuentes_tsv:
            grafo.agregar_vertice(int(linea[0]))
            if linea[0] == linea[1]: continue
            grafo.agregar_vertice(int(linea[1]))
            grafo.agregar_arista(int(linea[0]), int(linea[1]))                
    return grafo

#FUNCIONA OK
def min_seguimientos(grafo, origen, destino):
    resultado = []
    cadena = ""
    orden, padres = grafo.bfs(origen)
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

#FUNCIONA OK
def divulgar(grafo, delincuente, n):
    distancias,padres = grafo.bfs(delincuente)
    resultado = ""
    for vertice in distancias:
        if vertice == delincuente: continue
        if distancias[vertice] <= n: resultado += str(vertice) + ", "
    resultado = resultado[:-2]
    print(resultado)

#FUNCIONA OK
def cfc(grafo):
    visitados = set()
    orden = {}
    lista1 = []
    lista2 = []
    cfcs = []
    en_cfs = set()
    resultado = ""
    for vertice in grafo.vertices:
        if vertice not in visitados:
            orden[vertice] = 0
            dfs_cfc(grafo.vertices, vertice, visitados, orden, lista1, lista2, cfcs, en_cfs)
    for index, cfc in enumerate(cfcs):
        resultado = "CFC " + str(index + 1) + ": "
        for index,num in enumerate(cfc): 
            resultado += str(num) + ", "
        print(resultado[:-2])

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

    if lista1[-1] == vertice:
        lista1.pop()
        aux = None
        nueva_cfc = []
        while aux != vertice:
            aux = lista2.pop()
            en_cfs.add(aux)
            nueva_cfc.append(aux)
        cfcs.append(nueva_cfc)

#LABURANDO ACA
def random_walks(grafo, origen, largo):
    recorrido = {}
    v = origen
    for i in range(largo):
        adyacentes = grafo.adyacentes(v)
        if not v in recorrido: 
            recorrido[v] = 1
        else: 
            recorrido[v] += 1
        if len(adyacentes) > 0: 
            v = random.choice(adyacentes)
    return recorrido
        
def mas_imp(grafo, cantidad):
    apariciones = {}
    resultado = ""
    for actual in grafo.vertices:
        recorridos = random_walks(grafo, actual, 100)
        for v, aparicion in recorridos.items(): 
            if not v in apariciones:
                apariciones[v] = aparicion
            else:
                apariciones[v] += aparicion
    apariciones = sorted(apariciones.items(), key = operator.itemgetter(1), reverse = True)
    for index, delincuente in enumerate(apariciones):
        if index >= cantidad: break
        print(apariciones[index])
        resultado += str(apariciones[index][0]) + ", "
    resultado = resultado[:-2]
    print(resultado)
    

def divulgar_ciclo(grafo, delincuente, n):
    resultado = grafo.obtener_ciclo_bfs()
    print(resultado)
        
def comunidades(grafo, n):
    label = {}
    #inicio el dicc label con clave vertice y valor su indice en el dicc de grafo.vertices
    for index, clave in enumerate(grafo.vertices): label[clave] = index
    for i in range(CANT_ITERACIONES_COMUNIDADES): #esta es la parte de iterar varias veces
        claves = list(label.keys())
        random.shuffle(claves)
        for x in range(len(claves)): #voy actualizando el valor del vertice en el dicc con la max_freq de los labesl de sus adyacentes
            actual = claves[x]
            lista_aux = []
            for adyacente in grafo.vertices[actual]: lista_aux.append(label[adyacente])
            if max_freq(lista_aux) == None: continue
            label[actual] = max_freq(lista_aux)
    #recorro el dicc label y voy metiendo las comunidades(que son listas) en una lista de comunidades
    dicc_de_comunidades = {}
    for vertice in label:
        etiqueta = label[vertice]
        if not etiqueta in dicc_de_comunidades:
            comunidad = []
            comunidad.append(vertice)
            dicc_de_comunidades[etiqueta] = comunidad
        else:
            dicc_de_comunidades[etiqueta].append(vertice)
    #por ultimo tengo que devolver las comunidades que tengan al menos n vertices
    contador = 1
    for comunidad in dicc_de_comunidades.values():
        if len(comunidad) >= n:
            print("Comunidad " + str(contador) + ": " + str(comunidad))
            contador += 1
        
def max_freq(lista):
    resultado = collections.Counter(lista)
    etiqueta_que_mas_se_repite = -1
    cant_veces = -1
    for clave,valor in resultado.items():
        if valor > cant_veces:
            cant_veces = valor
            etiqueta_que_mas_se_repite = clave
    if etiqueta_que_mas_se_repite == -1: return None
    return etiqueta_que_mas_se_repite

main()