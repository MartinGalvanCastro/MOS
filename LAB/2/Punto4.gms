$ontext
Punto 4:
Suponga que el gobernador de un departamento de 6 pueblos desea determinar en
cuál de ellos debe poner una estación de bomberos. Para ello la gobernación desea
construir la mínima cantidad de estaciones que asegure que al menos habrá una estación
dentro de 15 minutos (tiempo para conducir) en cada pueblo.
$offtext

Sets
    i   ciudades /c1*c6/;
alias(i,j);
Scalar TMAX tiempoMaximo /15/;

Table T(i,j) "tiempo (min)"
    c1  c2  c3  c4  c5  c6
c1  0   10  20  30  30  20
c2  10  0   25  35  20  10
c3  20  25  0   15  30  20
c4  30  35  15  0   15  25
c5  30  20  30  15  0   14
c6  20  10  20  25  14  0
;

Variables
    x(i)    Indica si la estación se va a construir en el pueblo i
    z       Función Objetivo;

Binary Variable x(i);

Equations

FO     FuncioObjetivo
r      Restriccion de tiempo;

FO          ..z=e=sum(i,x(i));
r(i)        ..sum(j$(T(i,j)<=TMAX) ,x(j))=g=1

Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;

