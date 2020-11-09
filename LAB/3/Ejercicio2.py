"""
Ejercicio 2
Una empresa requiere cierto número de trabajadores que laboren durante 8 horas diarias en diferentes días de la semana. 
Los trabajadores deben desempeñar sus cargos 5 días consecutivos y descansar 2 días. Por ejemplo, un trabajador que labora 
de martes a sábado, descansaría el domingo y el lunes
"""

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

M = ConcreteModel()

dias=7

M.dias=RangeSet(1,dias)

#Trabajadores Por Dia
M.TPD=Param(M.dias,mutable=True)

M.TPD[1]=17
M.TPD[2]=13
M.TPD[3]=15
M.TPD[4]=19
M.TPD[5]=14
M.TPD[6]=16
M.TPD[7]=11

M.T = Param(M.dias,M.dias,mutable=True)
for i in M.dias:
    for j in M.dias:
        M.T[i,j]=0
    
for i in M.dias:
    M.T[i,i]=1
    aux = [i-j for j in range(1,5)]
    for j in aux:
        if j==0:
            M.T[i,7]=1
        else:
            M.T[i,(j%7)]=1
        
M.x=Var(M.dias,domain=PositiveIntegers)
M.obj=Objective(expr=sum(M.x[i] for i in M.dias),sense=minimize)
M.res=ConstraintList()
for i in M.dias:
    M.res.add( sum(M.x[j]*M.T[i,j] for j in M.dias)>= M.TPD[i])

SolverFactory('glpk').solve(M)

M.display()