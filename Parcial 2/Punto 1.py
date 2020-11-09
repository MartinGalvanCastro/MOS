# -*- coding: latin-1 -*-
"""
Parcial 2
Desarollado Por: 
    -Martin Galvan
    -Tomas Kavangh

Punto 1: Minima Potencia Disipada
"""

'''
Ecuaciones:
    -P=R*I^2
    -V=RI
    -V1=V2=V3
    -sum([1,3],Ii)==I4
'''

#Dependecias:
from pyomo.environ import *
from pyomo.opt import SolverFactory


LimInf=2
LimSup=10
numR=4  #Numero de resistencias
N = RangeSet(1,4)
I = {1:4,  #Corrientes en cada resistenci
              2:6,
              3:8,
              4:18}

modelo = ConcreteModel(name="Minima Potencia Disipada")
modelo.x=Var(N,domain=PositiveReals)    #Valor de la resistencia


# Funciones de Restricción
def voltajeRango(Modelo,i):
    '''
    Función de Rango del Voltaje
    '''
    return (LimInf,Modelo.x[i]*I[i],LimSup)
    
def igualdadVoltajes(Modelo,i):
    '''
    Función para hacer igualdad entre los voltajes
    '''
    if i<=2:
        return Modelo.x[i]*I[i]==Modelo.x[i+1]*I[i+1]
    else:
        return Constraint.Skip



modelo.z = Objective(expr = sum(modelo.x[i]*(I[i]**2) for i in N),sense=minimize)
modelo.voltajeRango=Constraint(N,rule=voltajeRango)
modelo.voltajeIgual=Constraint(N,rule=igualdadVoltajes)
SolverFactory('glpk').solve(modelo)
modelo.display()

print("########################################################################################")

print("El valor de los voltajes es: ")
for i in N:
    print("Voltaje " +str(i)+": ", value(modelo.x[i]))
    
print("La potencia disipada es: ",value(modelo.z))


