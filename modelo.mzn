include "globals.mzn";

% Entrada
int: n;  % Tamaño de la matriz
array[1..n, 1..n] of int: segmento_poblacion;
array[1..n, 1..n] of int: entorno_empresarial;
int: num_existentes;  % Número de localizaciones actuales
array[1..num_existentes] of int: x_existente;
array[1..num_existentes] of int: y_existente;
int: num_nuevos;  % Número de nuevas localizaciones

% Variables
array[1..num_nuevos] of var 1..n: x_nuevo;
array[1..num_nuevos] of var 1..n: y_nuevo;

% Variables para almacenar las sumas
array[1..num_nuevos] of var int: suma_segmento;
array[1..num_nuevos] of var int: suma_entorno;

% Variable para ordenar índices de coordenadas existentes
array[1..num_existentes] of int: indices_existentes = 1..num_existentes;
constraint forall(i, j in indices_existentes where i < j)(
    (x_existente[i] < x_existente[j]) \/
    (x_existente[i] == x_existente[j] /\ y_existente[i] <= y_existente[j])
);

% Variable para ordenar índices de coordenadas nuevas
array[1..num_nuevos] of int: indices_nuevas = 1..num_nuevos;
constraint forall(i, j in indices_nuevas where i < j)(
    (x_nuevo[i] < x_nuevo[j]) \/
    (x_nuevo[i] == x_nuevo[j] /\ y_nuevo[i] <= y_nuevo[j])
);

% Restricciones
constraint forall(i in 1..num_nuevos)(
    suma_segmento[i] = sum(dx in -1..1, dy in -1..1 where
        x_nuevo[i] + dx > 0 /\ x_nuevo[i] + dx <= n /\
        y_nuevo[i] + dy > 0 /\ y_nuevo[i] + dy <= n)
        (segmento_poblacion[x_nuevo[i] + dx, y_nuevo[i] + dy]) /\
    
    suma_entorno[i] = sum(dx in -1..1, dy in -1..1 where
        x_nuevo[i] + dx > 0 /\ x_nuevo[i] + dx <= n /\
        y_nuevo[i] + dy > 0 /\ y_nuevo[i] + dy <= n)
        (entorno_empresarial[x_nuevo[i] + dx, y_nuevo[i] + dy]) /\
    
    suma_segmento[i] >= 25 /\
    suma_entorno[i] >= 20
);

constraint forall(i, j in 1..num_nuevos where i < j)(
    abs(x_nuevo[i] - x_nuevo[j]) > 1 \/
    abs(y_nuevo[i] - y_nuevo[j]) > 1
);

constraint forall(i in 1..num_nuevos)(
    forall(j in 1..num_existentes)(
        abs(x_nuevo[i] - x_existente[j]) > 1 \/
        abs(y_nuevo[i] - y_existente[j]) > 1
    )
);

% Función objetivo
var int: ganancia_sin_nuevas = sum(j in 1..num_existentes)(
    sum(dx in -1..1, dy in -1..1 where
        x_existente[j] + dx > 0 /\ x_existente[j] + dx <= n /\
        y_existente[j] + dy > 0 /\ y_existente[j] + dy <= n)
        (segmento_poblacion[x_existente[j] + dx, y_existente[j] + dy] +
         entorno_empresarial[x_existente[j] + dx, y_existente[j] + dy])
);

var int: ganancia_total = ganancia_sin_nuevas + sum(i in 1..num_nuevos)(
    suma_segmento[i] + suma_entorno[i]
);

solve maximize ganancia_total;

output [
    show(ganancia_sin_nuevas), "\n",  % Ganancia sin nuevas localizaciones
    show(ganancia_total), "\n",       % Ganancia con nuevas localizaciones
    % Coordenadas de localizaciones existentes, una por línea
    concat([ show(x_existente[i]) ++ " " ++ show(y_existente[i]) ++ "\n" | i in 1..num_existentes ]),
    % Coordenadas de localizaciones nuevas, una por línea
    concat([ show(x_nuevo[i]) ++ " " ++ show(y_nuevo[i]) ++ "\n" | i in 1..num_nuevos ])
];
