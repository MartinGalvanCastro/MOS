$onText
Una empresa requiere cierto número de trabajadores que laboren durante 8 horas diarias en diferentes días de la semana.
Los trabajadores deben desempeñar sus cargos 5 días consecutivos y descansar 2 días.
Por ejemplo, un trabajador que labora de martes a sábado, descansaría el domingo y el lunes.
La cantidad mínima de trabajadores de tiempo completo requeridos por día de la semana se muestran a continuación:
$offtexT

Set i dias /D1*D7/;
alias(j,i);

Parameter d(i) trabajadoresPorDia
          /D1 17,D2 13,D3 15,D4 19,D5 14,D6 16,D7 11/;
        
          
Table T(i,j) "dias disponibles"
    D1  D2  D3  D4  D5  D6  D7
D1  1   0   0   1   1   1   1
D2  1   1   0   0   1   1   1
D3  1   1   1   0   0   1   1
D4  1   1   1   1   0   0   1
D5  1   1   1   1   1   0   0
D6  0   1   1   1   1   1   0
D7  0   0   1   1   1   1   1
;

Variables
    x(i)    # de trabajadores
    z       Función Objetivo;

Integer Variable x(i);

Equations
FO  Función de restricción
res Restricciones;

FO  ..z=e=sum(i,x(i));
res(i)  ..sum(j,T(i,j)*x(j))=g=d(i);


Model model1 /all/ ;
option mip=CPLEX
Solve model1 using mip minimizing z;

Display x.l;
Display z.l;






