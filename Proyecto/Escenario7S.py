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
def print_campo(Model,nFilas):
    for i in nFilas:
        aux = list(Model.mapa[i,:])
        aux2 = map(value,aux)
        print(list(aux2))


#Actualiza el mapa de Juego
def actualizarMapa(Model,nFilas,nColumnas):
    for i in nFilas:
        for j in nColumnas:
            Model.mapa[i,j]+=value(Model.x[i,j])
            if value(Model.mapa[i,j])>0:
                Model.mapa[i,j]=1

#FUNCION ELIMINAR COMPONENTE
def delete_component(Model, comp_name):

        list_del = [vr for vr in vars(Model)
                    if comp_name == vr
                    or vr.startswith(comp_name + '_index')
                    or vr.startswith(comp_name + '_domain')]

        list_del_str = ', '.join(list_del)

        for kk in list_del:
            Model.del_component(kk)


#Cargar parametro Escenario en el modelo  
def cargar_escenarioModel(Model,nFilas,nColumnas,escenario):
    
    if escenario == 1:       #Espacio vacio en el medio, sive para d, T, I
        for i in nFilas:
            for j in nColumnas:
                if i==24 and j!=5:
                    Model.mapa[i,j]=1
                else:
                    Model.mapa[i,j]=0
    elif escenario == 2:              #Dos espacios vacios separados
        for i in nFilas:
            for j in nColumnas:
                if i==24 and j not in [2,8]:
                    Model.mapa[i,j]=1
                else:
                    Model.mapa[i,j]=0
                        
    elif escenario == 3:              #Poner un O,una S o una Z
        for i in nFilas:
            for j in nColumnas:
                if i==24 and j not in [2,3]:
                    Model.mapa[i,j]=1
                else:
                    Model.mapa[i,j]=0 
    
    elif escenario == 4:              #Poner un cubo,una L o una J
        for i in nFilas:
            for j in nColumnas:
                if i==24 and j not in [2,3,4]:
                    Model.mapa[i,j]=1
                else:
                    Model.mapa[i,j]=0
 

#Cargar parametro matriz puntaje               
def cargarPuntajeModel(Model,nFilas,nColumnas):
    for i in nFilas:
        for j in nColumnas:
            Model.puntaje[i,j] = round((100/23) * (i-1),0)

def print_pieza(pieza):
    print("Pieza a poner:")
    try:
        fil,col = pieza.shape
        for i in range(fil):
            print(pieza[i,:])
    except:
        fil = pieza.shape[0]
        for i in range(fil):
            print([pieza[i]])


#Rota una pieza
def rotar_pieza(pieza,rotacion):
    if rotacion == 0:
        return pieza
    elif rotacion ==1:
        return np.transpose(pieza)
    elif rotacion ==2:
        return pieza[::-1,:]
    elif rotacion ==3:
        return np.transpose(pieza)[:,::-1]
    else:
        raise ValueError("Las rotaciones son validas desde 0 hasta 3")
        
def ultimaFilaLlena(Model,nFilas,nColumnas):
    """
    Metodo que devuelve la ultima fila llena

    Parameters
    ----------
    Model : TYPE
        DESCRIPTION.
    nFilas : TYPE
        DESCRIPTION.
    nColumnas : TYPE
        DESCRIPTION.

    Returns
    -------
    fila : TYPE
        DESCRIPTION.

    """
    fila=-1
    for i in nFilas:
        sumaFila = sum(Model.mapa[i,j] for j in nColumnas)
        if value(sumaFila)==10 and fila<i:
            fila = i-1
    if fila==-1:
        fila=24
    return fila

#%% Variables y Parametros del modelo
    
filas = 24
columnas=10
rotaciones=3
nFilas = RangeSet(1,filas)
nColumnas = RangeSet(1,columnas)
nRotacion = RangeSet(0,3)
entrada=['s0']
piezas = {'t0':np.array([[1,1,1],[0,1,0]]),
          't1':np.array([[1,0],[1,1],[1,0]]),
          't2':np.array([[0,1,0],[1,1,1]]),
          't3':np.array([[0,1],[1,1],[0,1]]),
          'z0':np.array([[1,1,0],[0,1,1]]),
          'z1':np.array([[0,1],[1,1],[1,0]]),
          'z2':np.array([[1,1,0],[0,1,1]]),
          'z3':np.array([[0,1],[1,1],[1,0]]),
          'i0':np.array([[1],[1],[1],[1]]),
          'i1':np.array([[1,1,1,1]]),
          'i2':np.array([[1],[1],[1],[1]]),
          'i3':np.array([[1,1,1,1]]),
          'l0':np.array([[1,0,0],[1,1,1]]),
          'l1':np.array([[1,1],[1,0],[1,0]]),
          'l2':np.array([[1,1,1],[0,0,1]]),
          'l3':np.array([[0,1],[0,1],[1,1]]),
          'j0':np.array([[0,0,1],[1,1,1]]),
          'j1':np.array([[1,1],[0,1],[0,1]]),
          'j2':np.array([[1,1,1],[1,0,0]]),
          'j3':np.array([[1,0],[1,0],[1,1]]),
          's0':np.array([[0,1,1],[1,1,0]]),
          's1':np.array([[1,0],[1,1],[0,1]]),
          's2':np.array([[0,1,1],[1,1,0]]),
          's3':np.array([[1,0],[1,1],[0,1]]),
          'o':np.array([[1,1],[1,1]]),
          'd':np.array([1])
    }




#%% Modelo Matematico

modelo = ConcreteModel()
modelo.puntaje = Param(nFilas,nColumnas,mutable=True)
modelo.mapa = Param(nFilas,nColumnas,mutable=True)
cargarPuntajeModel(modelo,nFilas,nColumnas)
cargar_escenarioModel(modelo,nFilas,nColumnas,3)
while(len(entrada)>0):
    
    fichaNueva = entrada[0]
    
    print("-----------------ESTADO INICIAL-------------")
    print_campo(modelo,nFilas)
    print("------------------------------------------------------")
    print_pieza(piezas[fichaNueva])
    print("-----------------MODELO-------------")
    
    #Variable de Desición
    modelo.x=Var(nFilas,nColumnas,domain=Binary) #Se pone o no pieza en esa casilla


    #Funcion(es) Objetivo
    modelo.ob = Objective(expr = sum((modelo.x[i,j])*modelo.puntaje[i,j] for j in nColumnas for i in nFilas), sense = maximize)

    #Restricciones

    def sobreponer(Model,i,j):
        """
        Restricción para no sobreponer una ficha
        """
        if Model.mapa[i,j]==0:
            return Model.x[i,j]+Model.mapa[i,j]<=1
        else:
            return Constraint.Skip

    modelo.R1 = Constraint(nFilas,nColumnas,rule=sobreponer)


    def piezasNuevas(Model):
        """
        Restriccion para que marque con 1 solo el numero de casillas con 1 que tiene la pieza
        """
        totalNuevas = np.sum(piezas[fichaNueva])
        totalMapa = sum(modelo.mapa[i,j] for j in nColumnas for i in nFilas)
        return sum(Model.x[i,j] for j in nColumnas for i in nFilas) == totalNuevas + value(totalMapa)

    modelo.R2 = Constraint(rule=piezasNuevas)
   
    
    def actualizarModelo(Model,i,j):
        """
        Restriccion para poner en 1 las casillas que en el mapa estan en 1
        """
        if Model.mapa[i,j]==1:
            return Model.x[i,j]==1
        else:
            return Constraint.Skip
    modelo.R3 = Constraint(nFilas,nColumnas,rule=actualizarModelo)
            
    modelo.R4 = ConstraintList()
    numRes = 0
    
    casillasJugables=[]
    fila = ultimaFilaLlena(modelo,nFilas,nColumnas)
    for j in nColumnas:
        if value(modelo.mapa[fila,j])==0:
            casillasJugables.append((fila,j))
            
    
    casillas_expr_R5 = []
    
    for casilla in casillasJugables:
        i,j = casilla
        if fichaNueva == 't0' and i>1 and j>1 and j<10:
            modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
            modelo.R4.add(modelo.x[i-1,j-1]>=modelo.x[i,j])
            modelo.R4.add(modelo.x[i-1,j+1]>=modelo.x[i,j])
            casillas_expr_R5.append((i,j))
        elif (fichaNueva == 'i0' or fichaNueva == 'i3') and i>3:
            modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
            modelo.R4.add(modelo.x[i-2,j]>=modelo.x[i,j])
            modelo.R4.add(modelo.x[i-3,j]>=modelo.x[i,j])
            casillas_expr_R5.append((i,j))
        elif fichaNueva == 'o' and j<10  and value(modelo.mapa[i,j+1])==0:
            modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
            modelo.R4.add(modelo.x[i-1,j+1]>=modelo.x[i,j])
            modelo.R4.add(modelo.x[i,j+1]>=modelo.x[i,j])
            casillas_expr_R5.append((i,j))
        elif fichaNueva == 'z0' or fichaNueva== 'z3' and j<10 and j>1:
            vecinoPiso = value(modelo.mapa[i,j+1])
            if vecinoPiso==0:
                modelo.R4.add(modelo.x[i,j+1]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i-1,j-1]>=modelo.x[i,j])
                casillas_expr_R5.append((i,j))
        elif fichaNueva == 's0' or fichaNueva== 's3' and j<10 and j>1:
            vecinoPiso = value(modelo.mapa[i,j-1])
            if vecinoPiso==0:
                modelo.R4.add(modelo.x[i,j-1]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i-1,j+1]>=modelo.x[i,j])
                casillas_expr_R5.append((i,j))
        elif fichaNueva == 'l0' and j<9 and modelo.mapa[i,j]==0:
            vecinoPiso = value(modelo.mapa[i,j+1])+value(modelo.mapa[i,j+2])
            if vecinoPiso==0:
                modelo.R4.add(modelo.x[i,j+1]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i,j+2]>=modelo.x[i,j])
                casillas_expr_R5.append((i,j))
        elif fichaNueva == 'j0' and j>2 and modelo.mapa[i,j]==0:
            vecinoPiso = value(modelo.mapa[i,j-1])+value(modelo.mapa[i,j-2])
            if vecinoPiso==0:
                modelo.R4.add(modelo.x[i,j-1]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i-1,j]>=modelo.x[i,j])
                modelo.R4.add(modelo.x[i,j-2]>=modelo.x[i,j])
                casillas_expr_R5.append((i,j))
        elif fichaNueva=='d':
            casillas_expr_R5.append((i,j))                                                       
                
    if len(casillas_expr_R5)==0 and len(entrada)>0:
        raise Exception('Ninguna ficha fue valida, revisar entradas')
 
    modelo.R5 = Constraint(expr=sum(modelo.x[idx] for idx in casillas_expr_R5)==1)

    #Mostrar solucion del modelo
    SolverFactory('glpk').solve(modelo)
    #modelo.display()
    #modelo.pprint()
    print("-----------------ESTADO FINAL-------------")
    actualizarMapa(modelo,nFilas,nColumnas)
    print_campo(modelo,nFilas)
    print("------------------------------------------------------")
    print("------------------------------------------------------")
    delete_component(modelo,'x')
    delete_component(modelo,'ob')
    delete_component(modelo,'R1')
    delete_component(modelo,'R2')
    delete_component(modelo,'R3')
    delete_component(modelo,'R4')
    delete_component(modelo,'R5')
    entrada.pop(0)