$OnText
Suponga que un sistema de multiprocesamiento posee 3 procesadores origen desde los cuales es necesario enviar procesos tipo
“modo kernel” y tipo “modo usuario” a 2 procesadores destino. 

En los procesadores origen 1, 2 y 3 se disponen de 60, 80 y 50 procesos modo kernel, y 80, 50 y 50 procesos modo
usuario respectivamente. En los procesadores destino 1 y 2 se requieren respectivamente 100 y 90 procesos modo kernel,
y 60 y 120 procesos modo usuario.

T1=Procesos modo Kernel
T2=Procesos modo usuario
$OffText

Set i procesadoresOrigen /PO1*PO3/;
Set j procesadoresDestino /PD1*PD2/;
Set k tipoProceso /T1*T2/;

Table O(i,k)    "Procesos Salientes"
    T1  T2
PO1 60  80
PO2 80  50
PO3 50  50
;

Table D(j,k)    "Procesos entrantes"
    T1  T2
PD1 10  60
PD2 90  120
;


Table C(i,j)    "Costos procesadores"
    PD1 PD2 
PO1 300 500
PO2 200 300
PO3 600 300
;


Variables
    x(i,j,k) Cantidad de procesos tipo K que envian de I a J
    z       Función Objetivo;

Positive Variable x(i,j,k);

Equations
F       Función Objetivo
R1      Restricción de procesos T1 salientes
R2      Restricción de procesos T1 entrantes
R3      Restricción de procesos T2 salientes
R4      Restricción de procesos T2 entrantes;

F(k)        ..z=e=sum((i,j),x(i,j,k)*C(i,j));
R1(i)       ..sum(j,x(i,j,'T1'))=e=O(i,'T1');
R2(j)       ..sum(i,x(i,j,'T1'))=e=D(j,'T1');
R3(i)       ..sum(j,x(i,j,'T2'))=e=O(i,'T2');
R4(j)       ..sum(i,x(i,j,'T2'))=e=D(j,'T2');

Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;


Display x.l;
Display z.l;

