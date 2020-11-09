from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

M = ConcreteModel()

#Variables auxiliares
tKey='Tipo'
dKey='Duracion'
BR,RR='Blues Rock','Rock and Roll'
numCanciones = 8
limiteDuración = [14,16]

#Rango de X
M.n = RangeSet(1,numCanciones)

#Datos canciones
data={
      1:{tKey:[BR],dKey:4},
      2:{tKey:[RR],dKey:5},
      3:{tKey:[BR],dKey:3},
      4:{tKey:[RR],dKey:2},
      5:{tKey:[BR],dKey:4},
      6:{tKey:[RR],dKey:3},
      7:{tKey:[],dKey:5},
      8:{tKey:[BR,RR],dKey:4},
      }

#True: Lado A, False: Lado B
M.x=Var(M.n,domain=Binary)

#Función Objetivo
M.obj = Objective(expr=sum(M.x[i] for i in M.n))

#Restriccion: La duración del cassete debe ser al menos 14 min
M.res1=Constraint(expr = sum(M.x[i]*data[i][dKey] for i in M.n)>=14)

#Restricción: La duración debe ser menor a 16min
M.res2=Constraint(expr = sum(M.x[i]*data[i][dKey] for i in M.n)<=16)

#Restricción: Cada lada debe tener exactamente 2 canciones de blues
M.res3=Constraint(expr = sum(M.x[i] for i in M.n if BR in data[i][tKey])==2)

#Restricción: El lado A debe tener al menos 3 canciones de RR
M.res4=Constraint(expr = sum(M.x[i] for i in M.n if RR in data[i][tKey])>=3)

#Restricción: Si la canción 1 esta en el lado A
#               L->La canción 5 no esta en el lado A
M.res5=Constraint(expr = M.x[5]+M.x[1]<=1)

#Restricción: Si la cancion 2 y 4 estan en lado A,
#               L->La canción 1 debe estar en el lado B
M.res6=Constraint(expr = M.x[1]<=2-(M.x[2]+M.x[4]) )


SolverFactory('glpk').solve(M)

M.display()

ladoA = [{i:data[i]} for i in M.n if value(M.x[i])>0]
ladoB = [{i:data[i]} for i in M.n if value(M.x[i])==0]

print('---------------------------------------------------')
print('Lado A')
for i in ladoA:
    print('Canción: {}'.format(i))
print('---------------------------------------------------')
print('Lado B')
for i in ladoB:
    print('Canción: {}'.format(i))


