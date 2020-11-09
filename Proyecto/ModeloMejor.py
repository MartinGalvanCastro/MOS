#%%
'''
Desarollado Por:
	Martin Galvan-201614423
	Tomas Kavanagh-201615122
'''

# Inicialización: Se cargan funciones que se van a usar

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
    campoJuego[22:24,:9]=1
    return campoJuego
    
#Metodo que genera la matriz del puntaje    
def matrixPuntaje(filas,columnas):
    matrixPunt=np.zeros((filas,columnas))
    for a in range(filas):
        for b in range(columnas):
            matrixPunt[a,b]=(a)+1
    return matrixPunt

#Actualiza el mapa de Juego
def actualizarMapaPrint(Modelo,campoDeJuego):
    for i in nFilas:
        for j in nColumnas:
            campoDeJuego[i-1,j-1]+=value(Modelo.x[i,j])
    return campoDeJuego


#Rota una pieza
def rotar_pieza(pieza,rotacion):
    if rotacion == 0:
        return pieza
    elif rotacion ==1:
        return np.transpose(pieza)
    elif rotacion ==2:
        return pieza[::-1,::-1]
    elif rotacion ==3:
        return np.transpose(pieza)[::-1,::-1]
    else:
        raise ValueError("Las rotaciones son validas desde 0 hasta 3")
#%% Variables y Parametros del modelo
    
filas = 24
columnas=10
rotaciones=3
nFilas = RangeSet(1,filas)
nColumnas = RangeSet(1,columnas)
nRotacion = RangeSet(0,3)
campoDeJuego = cargar_escenario(filas,columnas)
matrixPuntaje= matrixPuntaje(filas,columnas)
entrada=['i']
piezas = {'t':np.array([[1,1,1],[0,1,0]]),
          'z':np.array([[1,1,0],[0,1,1]]),
          'i':np.array([[1],[1],[1],[1]]),
          'l':np.array([[1,0,0],[1,1,1]]),
          'j':np.array([[0,0,1],[1,1,1]]),
          's':np.array([[0,1,1],[1,1,0]]),
          'o':np.array([[1,1],[1,1]])
    }

#%% Funciones de restricciones
#Marca las casillas ocupadas en el mapa de juego como x=1. (Ya tiene una pieza)
def marcar_usadas(modelo,i,j):
    if  campoDeJuego[i-1,j-1] == 1:
        return modelo.x[i,j]==1
    else:
        return Constraint.Skip
    
#Validar Mapa, La suma del mundo + la suma de la variablde de desición solo puede ser 1 o 0. Jamas mayor.
#               Evita que se ponga una ficha en una celda no valida de juego
def validar_mapa(modelo,i,j):
    return sum(modelo.x[i,j]+campoDeJuego[i-1,j-1] for j in nColumnas for i in nFilas)<=1


#%% Modelo Matematico

modelo = ConcreteModel()

#Variable de Desición
modelo.x=Var(nFilas,nColumnas,domain=Binary) #Se pone o no pieza en esa casilla


#Funcion(es) Objetivo
modelo.ob = Objective(expr = sum(modelo.x[i,j]*matrixPuntaje[i-1,j-1] for j in nColumnas for i in nFilas), sense = maximize)

#Restricciones

#Marcas casillas ya usadas
modelo.marcar = Constraint(nFilas,nColumnas,rule=marcar_usadas)

#Validar todo el mapa para que no tenga sobrelapamiento
modelo.valido = Constraint(nFilas,nColumnas,rule=validar_mapa)

#Restriccion que verifica que la pieza con cierta rotación se pueda poner en el mapa

#%% Mostrar solucion del modelo
#SolverFactory('glpk').solve(modelo)
modelo.display()
print(actualizarMapaPrint(modelo,campoDeJuego))