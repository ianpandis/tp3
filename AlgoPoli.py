import csv
from Grafo import Grafo
import sys
import random
import collections
from biblioteca import *
import operator
CANT_ITERACIONES_COMUNIDADES = 20

def main():
    archivo = cargar_grafo(sys.argv[1])
    print("Comandos disponibles:\n\tmin_seguimientos origen destino\n\tmas_imp cant\n\tpersecucion del1,del2,del3,...,delN K\n\tcomunidades n\n\tdivulgar delincuente n\n\tdivulgar_ciclo delincuente n\n\tcfc")
    comando = input("Ingrese un comando o 't' para terminar:").split()
    while comando[0] != "t":
        if comando[0] == "min_seguimientos":
            print(min_seguimientos(archivo, int(comando[1]),int(comando[2])))
        if comando[0] == "mas_imp":
            print(mas_imp(archivo, int(comando[1])))
        if comando[0] == "persecucion":
            delincuentes = comando[1].split(",")
            delincuentes = [int(i) for i in delincuentes]
            print(persecucion(archivo, delincuentes, int(comando[2])))
        if comando[0] == "comunidades":
            comunidades(archivo, int(comando[1]))
        if comando[0] == "divulgar":
            print(divulgar(archivo, int(comando[1]), int(comando[2])))
        if comando[0] == "divulgar_ciclo":
            print(divulgar_ciclo(archivo, int(comando[1]),int(comando[2])))
        if comando[0] == "cfc":
            cfc(archivo)
        comando = input("Ingrese un comando o 't' para terminar:").split()


"""*********************************************************************************"""
"""*********************************************************************************"""
"""*********************************COMANDOS****************************************"""
"""*********************************************************************************"""
"""*********************************************************************************"""

#FUNCIONA OK
def min_seguimientos(grafo, origen, destino):
    resultado = []
    cadena = ""
    orden, padres = bfs(grafo,origen)
    if destino not in padres:
        return "Seguimiento Imposible"
        print("Seguimiento Imposible")
    resultado.insert(0, destino)
    padre = padres[destino]
    while padre != None:
        resultado.insert(0, padre)
        padre = padres[padre]
    largo_resultado = len(resultado)
    for indice in range(largo_resultado):
        cadena += str(resultado[indice])
        if indice + 1 != largo_resultado: cadena += " -> "
    return cadena
    

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
        resultado += str(apariciones[index][0]) + ", "
    resultado = resultado[:-2]
    return resultado
    
#LABURANDO ACA
def divulgar_ciclo(grafo, origen, largo):
    d = ciclo_n(grafo, origen, largo)
    d.reverse()
    res=""
    for x in d:
        res+=str(x)
        res+=" -> "
    return res[:-4]

def persecucion(grafo, delincuentes, k):
    lista_mas_imp = mas_imp(grafo,k).split(", ")
    lista_mas_imp.reverse() #Ahora estan de menos imp a mas imp
    res = "."
    res_aux = ""
    for delincuente in delincuentes:
        for mas_importante in lista_mas_imp:
            res_aux = min_seguimientos(grafo, int(delincuente), int(mas_importante))
            if res_aux == "Seguimiento Imposible":
                continue
            if len(res) == 1: 
                res = res_aux
                continue
            if len(res_aux) <= len(res):
                res = res_aux
    return res

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
        
#FUNCIONA OK
def divulgar(grafo, delincuente, n):
    distancias,padres = bfs(grafo, delincuente)
    resultado = ""
    for vertice in distancias:
        if vertice == delincuente: continue
        if distancias[vertice] <= n: resultado += str(vertice) + ", "
    resultado = resultado[:-2]
    return resultado
    

main()