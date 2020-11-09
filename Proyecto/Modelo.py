'''
Desarollado Por:
	Martin Galvan-201614423
	Tomas Kavanagh-201615122
'''

import numpy as np
from pyomo.environ import *

from pyomo.opt import SolverFactory

#Print del campo de juego
def print_campo(campoDeJuego):
    for i in campoDeJuego:
        print(i)

#carga escenario        
def cargar_escenario(filas,columnas):
    campoJuego = np.zeros((filas,columnas))
    campoJuego[23,:9]=1
    return campoJuego
    
#Metodo que genera la matriz del puntaje    
def matrixPuntaje(filas,columnas):
    matrixPunt=np.zeros((filas,columnas))
    for a in range(filas):
        for b in range(columnas):
            matrixPunt[a,b]=(a)
        

#marca usadas 
def marcar_usadas(Modelo,i,j,mapaJuego):
    if  mapaJuego[i,j] == 1:
        return Modelo.x[i,j]==0  


#verifica que los loques de entrada no tengan colision con los bloques en el tablero de juego
def valida(Modelo,i,j):
    return sum((((piezas[p][i,j] + campoDeJuego[i+posX,j+posY]) for i in j) for j in piezas[p])for p in entrada)<=1

#Actualiza el mapa de Juego
def actualizarMapaPrint(Modelo,mapaJuego):
    for i in nFilas:
        for j in nColumnas:
            mapaJuego[i-1,j-1]+=value(Modelo.x[i,j])
    return mapaJuego

#diomedes, salvame de esta
def sumar_ficha(posX, posY, campoJuego, pieza):
    campoJuego[23,:9]=1
    indiceY, indiceX = -1,-1
    for linea in pieza:
        indiceY=indiceY+1
        for celda in linea:
            indiceX=indiceX+1
            campoJuego[a+(indiceY),b+(indiceX)]=1
    return campoJuego;

def sum(Modelo,i,j):
    return sum((((piezas[p][i,j] + campoDeJuego[i+posX,j+posY]) for i in j) for j in piezas[p])for p in entrada)<=1
            
   

#Parametros
filas = 24
columnas=10
nFilas = RangeSet(1,24)
nColumnas = RangeSet(1,24)
campoDeJuego = cargar_escenario(filas,columnas)
posX, posY = 0,0
matrixPuntaje= matrixPuntaje()

N=1
entrada=['t']
#


print_campo(campoDeJuego)

piezas = {'t':np.array([[1,1,1],[0,1,0]]),
          'z':np.array([[1,1,0],[0,1,1]]),
          'i':np.array([[1],[1],[1],[1]]),
          'l':np.array([[1,0,0],[1,1,1]]),
          'j':np.array([[0,0,1],[1,1,1]]),
          's':np.array([[0,1,1],[1,1,0]]),
          'o':np.array([[1,1],[1,1]])
    }


modelo = ConcreteModel()

#Variable
modelo.x=Var(nFilas,nColumnas,domain=Binary)

modelo.ob = Objective(expr = sum((modelo.x[i,j]*matrixPuntaje[i,j] for j in columnas) for i in filas), sense = maximize)

#Restringe las casillas iniciales
modelo.marcadas = ConstraintList()
for i in nFilas:
    for j in nColumnas:
        if campoDeJuego[i-1,j-1]:
            modelo.marcadas.add(modelo.x[i,j]==campoDeJuego[i-1,j-1])



print(actualizarMapaPrint(modelo,campoDeJuego))