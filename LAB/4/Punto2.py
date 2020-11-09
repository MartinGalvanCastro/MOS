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

f1=[]
f2=[]

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
            

def inv_constraint(Model,i,j):
    return sum(Model.x[i,j,k] for k in K)<=inv[i,j]

def dem_constraint(Model,i,k):
    return sum(Model.x[i,j,k] for j in J)==dem[i,k]

##############################################################################


tipoPaquete = 2
nodoOrigen = 3
nodoDestino = 4
modelo = ConcreteModel()

I=RangeSet(1,tipoPaquete)
J=RangeSet(1,nodoOrigen)
K=RangeSet(1,nodoDestino)

epsilon = 7000

costo = {(1,1):10,(1,2):9,(1,3):10,(1,4):11,
        (2,1):9,(2,2):10,(2,3):11,(2,4):10,
        (3,1):11,(3,2):9,(3,3):10,(3,4):10}

delay ={(1,1):12,(1,2):14,(1,3):10,(1,4):11,
        (2,1):11,(2,2):8,(2,3):7,(2,4):13,
        (3,1):6,(3,2):11,(3,3):4,(3,4):15}

inv = {(1,1):60,(1,2):80,(1,3):50,
       (2,1):20,(2,2):20,(2,3):30}

dem = {(1,1):50,(1,2):90,(1,3):40,(1,4):10,
       (2,1):10,(2,2):20,(2,3):10,(2,4):30}

step=20 #Si se cambia el step, la grafica del frente Optimo pude obtener mas o menos puntos, ademas de cambiar su forma un poco

try:
    for lim in reversed(range(0,epsilon+1,step)):
        print('Epsilon: ',lim)
        modelo.x=Var(I,J,K,domain=PositiveIntegers)
        modelo.f1 = Objective(expr = sum(costo[j,k]*modelo.x[i,j,k] for i in I for j in J for k in K), sense = minimize)
        modelo.f2 = Constraint(expr = sum(delay[j,k]*modelo.x[i,j,k] for i in I for j in J for k in K)<=lim)
        modelo.inv = Constraint(I,J,rule=inv_constraint)
        modelo.dem = Constraint(I,K,rule=dem_constraint)
        SolverFactory('glpk').solve(modelo)
        modelo.display()
        f1 = f1 +[value(modelo.f1)]
        f2 = f2 +[value(modelo.f2)]
        delete_component(modelo, 'x')
        delete_component(modelo, 'f1')
        delete_component(modelo, 'f2')
        delete_component(modelo, 'inv')
        delete_component(modelo, 'dem')
except Exception:
    pass #Si entra aca es por que la solución no se puede determinar y ya se acabo la iteración
finally:
    plt.plot(f1,f2,'o-.')
    plt.title('Frente Óptimo de Pareto')
    plt.xlabel('F1')
    plt.ylabel('F2')
    plt.grid(True);
    plt.show()