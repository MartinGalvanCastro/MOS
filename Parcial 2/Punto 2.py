"""
Parcial 2
Desarollado Por: 
    -Martin Galvan
    -Tomas Kavangh

Punto 2: Domicilios
"""


#Dependecias:
from pyomo.environ import *
from pyomo.opt import SolverFactory
import plotly.graph_objects as go
import numpy as np
import sys
import os
from random import randint

#import ad

os.system("clear")

#sys.exit("Stopped")

Model = ConcreteModel()

# FUNCIONES**************************************************************************
def distancia(x1,x2):
    '''
    Retorna la distancia Euclidiana entre dos puntos

    Parameters
    ----------
    x1 : Tupla
        Coordenadas X1.
    x2 : Tupla
        Coordenadas X2.

    Returns
    -------
    Int
        Distancia redondeada al entero más cercano

    '''
    return round(np.linalg.norm(np.array(x1)-np.array(x2),2))


# SETS & PARAMETERS********************************************************************
nodos = {1:(10,50),
         2:(30,60),
         3:(50,60),
         4:(30,40),
         5:(50,40),
         6:(70,50)}

arcos = {1:[2,4],
         2:[1,4,3],
         3:[2,5,6],
         4:[1,2,5],
         5:[3,4,6],
         6:[3,5]
         }
nodosIniciales={1:1,2:4}
nodosFinales=[3,4,5,6]


N = RangeSet(1,len(nodos))  #Rango de Nodos
D=RangeSet(3,6)             #Nodos finales
R=RangeSet(1,2)             #Repartidores

'''
Calculo de costos
'''
costos = {i:{} for i in N}
for nodo in N:
    vecinos = arcos[nodo]
    for nodo2 in N:
        if nodo2 in vecinos:
            costos[nodo][nodo2]=distancia(nodos[nodo],nodos[nodo2])
        else:
            costos[nodo][nodo2]=999
            
# VARIABLE*****************************************************************************
Model.x=Var(R,N,N,domain=Binary)

# OBJETIVO*****************************************************************************
Model.func = Objective(expr = sum(Model.x[r,i,j]*costos[i][j] for j in N for i in N for r in R))

# RESTRICCIONES************************************************************************
def unPedido(Model,r):
    '''
    Todos los repartidores tienen que tener almenos un pedido
    '''
    return sum(Model.x[r,i,j] for j in N for i in N)>=1
Model.res1 = Constraint(R,rule=unPedido)

def unSentido(Model,r,i,j):
    '''
    Solo se puede atravezar el camino en sentido i->j o j->i
    '''
    return Model.x[r,i,j]+Model.x[r,j,i]<=1
Model.res2 = Constraint(R,N,N, rule = unSentido)

def unRepartidorCamino(Model,i,j):
    '''
    Un repartidor solo puede pasar por ese camino
    '''
    return sum(Model.x[r,i,j] for r in R)<=1
Model.res3 = Constraint(N,N,rule=unRepartidorCamino)

def recorrido(Model):
    '''
    Restriccion que asegura que existan las transiciones suficientes para atravezar el grafo
    '''
    return sum(Model.x[r,i,j] for j in N for i in N for r in R)==4
Model.res4 = Constraint(rule=recorrido)

def origen(Model,r,i):
    '''
    Un nodo origen solo puede ir a 1 nodo no origen
    Si el nodo origen no pertenece a ese repartidor, no puede salir a ningun lado de ese nodo
    Nadie puede acceder al nodo origen
    '''
    lista = list(nodosIniciales.values())
    if i in lista:
        if i==nodosIniciales[r]:
            return sum(Model.x[r,i,j] for j in N if j not in lista)==1
        else:
            return sum(Model.x[r,i,j] for j in N)==0
    else:
        return sum(Model.x[r,i,j] for j in N if j in lista)==0
Model.res5 =Constraint(R,N,rule=origen)


def unRepartidorEntra(Model,j):
    '''
    Solo el repartidor 1 o el 2 puede entrar al nodo J por cualquier camino
    '''
    lista = list(nodosIniciales.values())
    if j not in lista:
        return sum(Model.x[1,i,j] for i in N) + sum(Model.x[2,i,j] for i in N)<=1
    else:
        return Constraint.Skip
Model.res6 = Constraint(N,rule=unRepartidorEntra)


def unRepartidorSale(Model,i):
    '''
    Solo el repartidor 1 o el 2 puede salir del nodo I a cualquier otro
    '''
    lista = list(nodosIniciales.values())
    if i not in lista:
        return sum(Model.x[1,i,j] for j in N) + sum(Model.x[2,i,j] for j in N)<=1
    else:
        return Constraint.Skip
Model.res7 = Constraint(N,rule=unRepartidorSale)



def intermedio(Model,r,i):
    '''
    #Restriccion para asegurar continuidad en los flujos
    '''
    lista = list(nodosIniciales.values())
    if i not in lista:
        return sum(Model.x[r,i,j] for j in N if j not in lista) <= sum(Model.x[r,j,i] for j in N)
    else:
        return Constraint.Skip
Model.res8 = Constraint(R,N,rule=intermedio)



SolverFactory('glpk').solve(Model)
Model.display()


print("########################################################################################")
