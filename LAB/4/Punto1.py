'''
Desarollado Por:
	Martin Galvan-201614423
	Tomas Kavanagh-201615122
'''

from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory
from matplotlib import pyplot as plt

import sys
import os


##############################################################################
#####################        FUNCIONES        ################################
##############################################################################


#FUNCION ELIMINAR COMPONENTE
def delete_component(Model, comp_name):

        list_del = [vr for vr in vars(Model)
                    if comp_name == vr
                    or vr.startswith(comp_name + '_index')
                    or vr.startswith(comp_name + '_domain')]

        list_del_str = ', '.join(list_del)
        print('Deleting model components ({}).'.format(list_del_str))

        for kk in list_del:
            Model.del_component(kk)

##############################################################################

f1=[]
f2=[]

#Sets
numNodos =5
N = RangeSet(1,numNodos)
epsilon = 5
modelo = ConcreteModel()

hops={(1,1):999, (1,2):1,   (1,3):1,   (1,4):999, (1,5):999,
      (2,1):999, (2,2):999, (2,3):999, (2,4):999, (2,5):1,
      (3,1):999, (3,2):999, (3,3):999, (3,4):1,   (3,5):999,
      (4,1):999, (4,2):999, (4,3):999, (4,4):999, (4,5):1,
      (5,1):999, (5,2):999, (5,3):999, (5,4):999, (5,5):999}

cost={(1,1):999, (1,2):10,  (1,3):5,   (1,4):999, (1,5):999,
      (2,1):999, (2,2):999, (2,3):999, (2,4):999, (2,5):10,
      (3,1):999, (3,2):999, (3,3):999, (3,4):5,   (3,5):999,
      (4,1):999, (4,2):999, (4,3):999, (4,4):999, (4,5):5,
      (5,1):999, (5,2):999, (5,3):999, (5,4):999, (5,5):999}

def source_rule(Model,i):
    if i==1:
        return sum(Model.x[i,j] for j in N)==1
    else:
        return Constraint.Skip

def destination_rule(Model,j):
    if j==5:
        return sum(Model.x[i,j] for i in N)==1
    else:
        return Constraint.Skip

def intermediate_rule(Model,i):
    if i!=1 and i!=5:
        return sum(Model.x[i,j] for j in N) - sum(Model.x[j,i] for j in N)==0
    else:
        return Constraint.Skip



try:
    for i in reversed(range(epsilon+1)):
        print('Epsilon: ', i)
        #Variables
        modelo.x = Var(N,N, domain=Binary)
        #Función Objetivo
        modelo.f2 =Objective(expr = sum(modelo.x[i,j]*cost[i,j] for i in N for j in N))
        #Restricciones
        modelo.source=Constraint(N, rule=source_rule)
        modelo.destination=Constraint(N, rule=destination_rule)
        modelo.intermediate=Constraint(N, rule=intermediate_rule)    
        modelo.f1 =Constraint(expr = sum(modelo.x[i,j]*hops[i,j] for i in N for j in N)<=i)
        SolverFactory('glpk').solve(modelo)
        modelo.display()
        f1 = f1 +[value(modelo.f1)]
        f2 = f2 +[value(modelo.f2)]
        
        delete_component(modelo,'x')
        delete_component(modelo,'source') 
        delete_component(modelo,'destination')
        delete_component(modelo,'intermediate')
        delete_component(modelo,'f2')
        delete_component(modelo,'f1')
except Exception:      
     pass #Si entra aca es por que la solución no se puede determinar y ya se acabo la iteración
finally:
    plt.plot(f1,f2,'o-.')
    plt.title('Frente Óptimo de Pareto')
    plt.xlabel('F1')
    plt.ylabel('F2')
    plt.grid(True);
    plt.show()



