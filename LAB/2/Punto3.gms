$ontext
Suponga que conoce el mapa de la tubería de una sección de su
casa, y desea levantar la mínima cantidad de losas para conocer
el tipo de material del cual está hecho cada tubo.
$offtext

set i numeroFilas /f1*f5/;
set j numeroColumnas /c1*c4/;
set k numeroTuberiaa /t1*t7/;

parameter loza(i,j,k)   Hay tuberia en la loza. 0 no hay tuberia. 1 hay tuberia;

loza(i,j,k)=0;

loza('f1','c1','t1')=1;
loza('f2','c1','t1')=1;

loza('f1','c2','t2')=1;
loza('f1','c3','t2')=1;
loza('f2','c2','t2')=1;
loza('f2','c3','t2')=1;

loza('f2','c1','t3')=1;
loza('f3','c1','t3')=1;

loza('f3','c1','t4')=1;
loza('f3','c2','t4')=1;
loza('f4','c1','t4')=1;
loza('f4','c2','t4')=1;

loza('f3','c2','t5')=1;
loza('f3','c3','t5')=1;
loza('f4','c2','t5')=1;
loza('f4','c3','t5')=1;

loza('f4','c1','t6')=1;
loza('f5','c1','t6')=1;

loza('f2','c4','t7')=1;
loza('f3','c4','t7')=1;
loza('f4','c4','t7')=1;
loza('f5','c4','t7')=1;
loza('f5','c3','t7')=1;

Variables
    x(i,j)  Loza se levanto
    z       Función Objetivo

Binary Variable x(i,j);

Equations
FO  Función Objetivo
res Restricciones Tuberia;

FO  ..z=e=sum((i,j),x(i,j));
res(k)  ..sum((i,j),x(i,j)*loza(i,j,k))=g=1;

Model model1 /all/;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;