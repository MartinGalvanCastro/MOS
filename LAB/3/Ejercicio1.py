"""
Ejercicio 1
Suponga que el gobernador de un departamento de 6 pueblos desea determinar en cuál de ellos debe poner una estación de 
bomberos. Para ello la gobernación desea construir la mínima cantidad de estaciones que asegure que al menos habrá una 
estación dentro de 15 minutos (tiempo para conducir) en cada pueblo
"""


from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

M = ConcreteModel()

numPueblos = 6
M.p = RangeSet(1,numPueblos)
M.tiempo=Param(M.p, M.p, mutable=True)
            
for i in M.p:
    for j in M.p:
        M.tiempo[i,j]=0

M.tiempo[1,2]=10
M.tiempo[1,3]=20
M.tiempo[1,4]=30
M.tiempo[1,5]=30
M.tiempo[1,6]=20

M.tiempo[2,3]=25
M.tiempo[2,4]=35
M.tiempo[2,5]=20
M.tiempo[2,6]=10

M.tiempo[3,4]=15
M.tiempo[3,5]=30
M.tiempo[3,6]=20

M.tiempo[4,5]=15
M.tiempo[4,6]=25

M.tiempo[5,6]=14

for i in M.p:
    for j in M.p:
        M.tiempo[j,i]=M.tiempo[i,j]
        
        
#time = [[value(M.tiempo[i,j]) for j in M.p] for i in M.p]
        
M.x=Var(M.p,domain=Binary)
M.obj=Objective(expr= sum(M.x[i] for i in M.p),sense=minimize)
M.res = ConstraintList()
for i in M.p:
    M.res.add(sum(M.x[j] for j in M.p if value(M.tiempo[i,j])<=15) >= 1)

SolverFactory('glpk').solve(M)

M.display()
