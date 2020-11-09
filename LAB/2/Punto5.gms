$ontext
Cada enlace significa que entre un par de nodos existe conexión, la cual tiene un costo equivalente a la distancia
entre ese par de nodos. Para determinar si hay enlace entre un par de nodos, la distancia entre ellos debe ser menor o
igual a 20. Se requiere encontrar la ruta de mínimo costo entre los nodos 4 y 6. 
$offtext

set i nodos /n1*n7/;
alias(i,j)

Parameters
    x(i)    Posicion en X del nodo
            /n1 20,n2 22,n3 9,n4 3,n5 21,n6 29,n7 14/
    
    y(i)    Posicion en Y del nodo
            /n1 6,n2 1,n3 2,n4 25,n5 10,n6 2,n7 12/
    
    c(i,j)  Costo para del nodo I al nodo J;

c(i,j)=999;

scalar d;
loop(i,
    loop(j,
        d=(((x(i)-x(j))*(x(i)-x(j))) + ((y(i)-y(j))*(y(i)-y(j))))**(1/2) ;
        if(d<=20 and d<>0,
            c(i,j)=d;
        );
    );
);


Variables
  s(i,j)      Indicates if the link i-j is selected or not.
  z           Objective function  ;

Binary Variable s;

Equations
objectiveFunction        objective function
sourceNode(i)            source node
destinationNode(j)       destination node
intermediateNode         intermediate node;

objectiveFunction                                  ..  z =e= sum((i,j), c(i,j) * s(i,j));


sourceNode(i)$(ord(i) =4)   ..  sum((j), s(i,j)) =e= 1;

destinationNode(j)$(ord(j) = 6)                    ..  sum((i), s(i,j)) =e= 1;

intermediateNode(i)$(ord(i) <> 4 and ord(i) <> 6)  ..  sum((j), s(i,j)) - sum((j), s(j,i)) =e= 0;

Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display c;
Display s.l;
Display z.l;
