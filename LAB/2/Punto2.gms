$ontext
El entrenador de un equipo de básquetbol requiere escoger el equipo titular (5 de 7 jugadores) que jugará el siguiente partido.
El equipo total consta de siete jugadores que están clasificados (con una escala de 1=deficiente a 3= excelente)
de acuerdo  a sus habilidades técnicas tales como: control del balón, disparo, rebote y habilidades defensivas. 
$offtext

Set i jugadores /j1*j7/;
Set j atributos /a1*a4/;

parameter atq(i)    Jugadores que van en ataque
                    /j1 1, j2 0,j3 1,j4 0,j5 1,j6 0,j7 1/;
parameter cent(i)   Jugadores que van en centro
                    /j1 0, j2 1,j3 0,j4 1,j5 0,j6 1,j7 0/;
parameter def(i)    Jugadores que van en defenza
                    /j1 0, j2 0,j3 1,j4 1,j5 1,j6 1,j7 1/;
                    
Table P(i,j)    "Puntaje del jugador I en atributo J"
    a1  a2  a3  a4
j1  3   3   1   3
j2  2   1   3   2
j3  2   3   2   2
j4  1   3   3   1
j5  3   3   3   3
j6  3   1   2   3
j7  3   2   2   1
;

Variables
    x(i)    El jugador I fue elegido
    z       Variable objetivo;
    
Binary Variable x(i);

Equations

OF  Función Objetivo
R1  Tamaño del Equipo
R2  Almenos 4 Jugadores en la defenza
R3  Almenos 2 Jugadores al ataque
R4  Almenos 1 Jugador en el centro
R5  El promedio de atributos tiene que ser almenos de 2
R6  Juega el jugador 6 o 7;

OF                                  ..z=e=sum(i,x(i)*P(i,'a4'));
R1                                  ..sum(i,x(i))=e=5;
R2                                  ..sum(i,x(i)*def(i))=g=3;
R3                                  ..sum(i,x(i)*atq(i))=g=1;
R4                                  ..sum(i,x(i)*cent(i))=g=0;
R5(j)$(ord(j)>=1 and ord(j)<=3)     ..sum(i,x(i)*P(i,j))/5=g=1;
R6                                  ..sum(i$(ord(i)>=6 and ord(i)<=7),x(i))=l=2;

Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;
