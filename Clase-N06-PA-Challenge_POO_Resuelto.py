"""
En la clase vimos el desarrollo de un algoritmo genético para resolver el problema n-Reinas según el paradigma estructurado.

La idea de esta tarea es pasar ese código a un paradigma de orientación a objetos.
Se puede hacer de dos formas:
- Creando una sola clase (nReinas) que realice toda la tarea
  Esa única clase debería tener un constructor que tome como argumento el número de lados del tablero, y un método que muestre el resultado. (que dibuje el tablero solución, y alguna información adicional como el número de lados, la cantidad de iteraciones que hubo, y alguno que se les ocurra)
- Creando DOS clases. Una que represente al Tablero y que tenga todos los métodos y atributos que necesita tener el tablero (número de lados, mutar(), cruzar(), rankear(), etc)
  Y otra que sea haga lo mismo que nReinas, pero que use a Tablero. Por ejemplo, la población va a ser una lista conteniendo instancias de Tablero)

La tarea debe ser entregada antes de las 12:00 (mediodía) del viernes 7/06 en un solo archivo de forma nombre_apellido.py  a este correo.

Ya que compile y presente la información pedida asegura una nota alta, pero para el 10 sería necesario hacerlo usando las dos clases.
"""

import random
import time

class Tablero():
    def __init__(self, lados):
        self.lados = lados
        self.reinas = [random.randint(1, lados) for _ in range(lados)]
 
    def fitness(self):
        diagonal = 0
        horizontal = len(self.reinas) - len(set(self.reinas))
        numero = len(self.reinas)
        for i in range(numero):
            for j in range(i + 1, numero):
                if abs(i - j) == abs(self.reinas[i] - self.reinas[j]):
                    diagonal += 1
        return horizontal + diagonal 
    
    def mutar(self):
        indice_aleatorio = random.randint(0, self.lados - 1)
        nuevo_valor = random.randint(1, self.lados)
        self.reinas[indice_aleatorio] = nuevo_valor
        return self


class nReinas():  
    def __init__(self, lados, max_iteraciones, max_poblacion):
        self.lados = lados
        self.max_iteraciones = max_iteraciones
        self.max_poblacion = max_poblacion  
        
        self.poblacion = []
        for _ in range(max_poblacion):
            un_tablero = Tablero(lados)
            self.poblacion.append(un_tablero)
    
    def rankeador(self):
        salida = []
        for tablero in self.poblacion:
            ranking = tablero.fitness()
            salida.append((tablero, ranking))
        poblacion_ordenada = sorted(salida, key=lambda x: x[1])
        return poblacion_ordenada
    
    def cruzaYMuta(self):
        mitad = self.max_poblacion // 2
        medio = self.lados // 2
        mejores = self.rankeador()[:mitad]
        nueva_poblacion = []
        
        for indice in range(1, mitad, 2):
            # Sacamos de a pares los mejores
            madre = mejores[indice][0].reinas
            padre = mejores[indice - 1][0].reinas
        
            # Generamos los hijos
            hijo1_tablero = madre[:medio] + padre[medio:]
            hijo2_tablero = padre[:medio] + madre[medio:]
            
            # Creamos las nuevas instancias de Tablero
            hijo1 = Tablero(self.lados)
            hijo1.reinas = hijo1_tablero
            hijo2 = Tablero(self.lados)
            hijo2.reinas = hijo2_tablero
            
            # Aplica una mutación al azar
            azar = random.random()
            if azar > 0.70:
                hijo1.mutar()
                hijo2.mutar()
                
            # Armamos la nueva población
            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)
        
        # Reemplazamos la población antigua con la nueva
        self.poblacion = nueva_poblacion
    
    def dibujo(self, tablero):
        # Separamos las partes (esta rankeado)
        tab = tablero.reinas
        ranking = tablero.fitness()
        # Genera el tablero
        n = len(tab)
        dibujo = []
        for i in range(n):
            dibujo.append(list("." * n))
            for k in range(n):
                if tab[k] - 1 == i:
                    dibujo[i][k] = "R"
            dibujo[i] = " ".join(dibujo[i])
        
        return "\n".join(dibujo) + "\nFitness: " + str(ranking)
    
    def resultado(self):
        solucionesRank = self.rankeador()
        for generacion in range(self.max_iteraciones):
            if solucionesRank[0][1] == 0:
                print(f"Se completaron {generacion + 1} generaciones")
                print(self.dibujo(solucionesRank[0][0]))
                return
            
            self.cruzaYMuta()
            solucionesRank = self.rankeador()
        
        print("No se encontró solución óptima.")


# Prueba del código

# 4 lados, con 5000 iteraciones y 50 poblaciones
mytablero = nReinas(4, 5000, 50)
mytablero.resultado()

print("-----------------------------------")

# 8 lados, con 10000 iteraciones y 100 poblaciones
mytablero = nReinas(8, 10000, 100)
mytablero.resultado()

time.sleep(1)