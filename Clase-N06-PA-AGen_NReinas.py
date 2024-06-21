#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:15:25 2024

@author: Raul Marusca
"""
# Importamos librerias
import random

# Valores iniciales
MAXIMO_ITERACIONES = 5000
MAXIMO_POBLACION  = 50
LADO = 8
# #############################################################################
# funcion que genera un tablero al azar (cromosoma)
def tableroAzar(lado):
    return [ random.randint(1, lado) for _ in range(lado) ]
# si fuera de 4 el lado:
# ...R
# R...
# .R..
# ..R.
# [3,2,1,4]

# Funcion que evalua el fitness del tablero
def fitness(tablero):
    diagonal = 0
    horizontal = len(tablero) - len(set(tablero)) #4-3
    numero = len(tablero)
    for indiceI in range(numero): # Recorre las columnas
        for indiceJ in range(indiceI + 1, numero): # de la columna al final
            # Esta es la ecuacion de las diagonales
            if (abs(indiceI - indiceJ) == abs(tablero[indiceI] - tablero[indiceJ])): 
                diagonal += 1 
    return horizontal + diagonal
# [3,1,4,2]
#  0 1      0-1  3-1 abs 1 != 2
#  0   2    0-2  3-4 abs 2 != 1
#  0     3  0-3  3-2 abs 3 != 1 

#    1 2    1-2  1-4 abs 1 != 3
#    1   3  1-3  1-2 abs 2 != 1

#      2 3  2-3  4-2 abs 1 != 2 

# Esta funcion muta un tablero
def mutarTablero(tablero):
    indiceAleatorio = random.randint(0, LADO - 1)
    nuevoValor = random.randint(1, LADO)
    tablero[indiceAleatorio] = nuevoValor
    return tablero
# [2,5,6,3,2,4]
#      2 -> (4)

# Funcion que genera un numero de posibles soluciones 
def poblacionInicial(lado):
    poblacion = []
    for _ in range(MAXIMO_POBLACION):
       unTablero = tableroAzar(lado)
       poblacion.append(unTablero)
    return poblacion
       
# Esta funcion ranquea la poblacion y la ordena de menor a mayor   
def rankeador(poblacion):
    salida = []
    for elemento in poblacion:       
       ranking = fitness(elemento)
       salida.append((elemento,ranking))
    # ordeno por el fitness
    poblacionOrdenada = sorted(salida, key=lambda x: x[1])
    # retorno la lista ordenada
    return poblacionOrdenada
# [([tablero], ranking),
#  ([tablero], ranking),
#  ([tablero], ranking),...
# ]  

      
# funcion cruza y muta los mejores tableros
def cruzaYMuta(poblacionOrdenada):
    mitad = MAXIMO_POBLACION // 2
    medio = LADO // 2
    mejores = poblacionOrdenada[:mitad]
    salida = []
    
    for indice in range(1,mitad,2):
        # Sacamos de a pares los mejores
        madre = mejores[indice][0]
        padre = mejores[indice-1][0]
        # generamos los hijos
        hijo1 = madre[:medio] + padre[medio:]
        hijo2 = padre[:medio] + madre[medio:]
        # aplica una mutacion al azar
        azar = random.random()
        if azar > 0.70:
            hijo1 = mutarTablero(hijo1)
            hijo2 = mutarTablero(hijo2)     
        # armamos la salida (solo poblacion)
        salida.append(hijo1)
        salida.append(hijo2)       
    
    return salida

# Funcion que imprime el tablero rankeado
def dibujo(tablero):
    # Separamos las partes (esta rankeado)
    tab = tablero[0]
    ranking = tablero[1]
    # genera el tablero
    n = len(tab)
    dibujo = []
    for i in range(n):
        dibujo.append(list("."*n))
        for k in range(n):
            if tab[k] - 1 == i:
                dibujo[i][k]="R"
        dibujo[i]=" ".join(dibujo[i])
# ...R R... .R.. ..R.
# ...R
# R...
# .R..
# ..R.
# fitness: 3
    return "\n".join(dibujo)+"\nfitness: " + str(ranking) 
# #############################################################################

# Creamos la poblacion inicial
soluciones = poblacionInicial(LADO)

# la rankeamos
solucionesRank = rankeador(soluciones)

# repetimos hasta agotar el numero de iteraciones
for generacion in range(MAXIMO_ITERACIONES):
    # chequeamos si hay una solucion optima
    if solucionesRank[0][1] == 0:
        # dibujamos el tablero ganador
        print(dibujo(solucionesRank[0]))
        break
    # Como no hay una solucion, reemplazamos la poblacion por la nueva
    soluciones = cruzaYMuta(solucionesRank)
    # rankeamos las soluciones
    solucionesRank = rankeador(soluciones)
    
# Se informa del numero de generaciones
print(f"Se completaron {generacion + 1} generaciones")
