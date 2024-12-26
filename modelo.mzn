% Entrada
int: n;  % Tamaño de la matriz (0 a n-1)
array[0..n-1, 0..n-1] of int: segmento_poblacion;
array[0..n-1, 0..n-1] of int: entorno_empresarial;
int: num_existentes;  % Número de localizaciones actuales
array[0..num_existentes-1] of int: x_existente;
array[0..num_existentes-1] of int: y_existente;
int: num_nuevos;  % Número de nuevas localizaciones

% Variables
array[0..num_nuevos-1] of var 0..n-1: x_nuevo;
array[0..num_nuevos-1] of var 0..n-1: y_nuevo;

% Variables para almacenar las sumas
array[0..num_nuevos-1] of var int: suma_segmento;
array[0..num_nuevos-1] of var int: suma_entorno;

% Restricciones
constraint forall(i in 0..num_nuevos-1)(
    suma_segmento[i] = sum(dx in -1..1, dy in -1..1 where
        x_nuevo[i] + dx >= 0 /\ x_nuevo[i] + dx < n /\
        y_nuevo[i] + dy >= 0 /\ y_nuevo[i] + dy < n)
        (segmento_poblacion[x_nuevo[i] + dx, y_nuevo[i] + dy]) /\
    
    suma_entorno[i] = sum(dx in -1..1, dy in -1..1 where
        x_nuevo[i] + dx >= 0 /\ x_nuevo[i] + dx < n /\
        y_nuevo[i] + dy >= 0 /\ y_nuevo[i] + dy < n)
        (entorno_empresarial[x_nuevo[i] + dx, y_nuevo[i] + dy]) /\
    
    suma_segmento[i] >= 25 /\
    suma_entorno[i] >= 20
);

constraint forall(i, j in 0..num_nuevos-1 where i < j)(
    abs(x_nuevo[i] - x_nuevo[j]) > 1 \/
    abs(y_nuevo[i] - y_nuevo[j]) > 1
);

constraint forall(i in 0..num_nuevos-1)(
    forall(j in 0..num_existentes-1)(
        abs(x_nuevo[i] - x_existente[j]) > 1 \/
        abs(y_nuevo[i] - y_existente[j]) > 1
    )
);

% Función objetivo
var int: ganancia_sin_nuevas = sum(j in 0..num_existentes-1)(
    sum(dx in -1..1, dy in -1..1 where
        x_existente[j] + dx >= 0 /\ x_existente[j] + dx < n /\
        y_existente[j] + dy >= 0 /\ y_existente[j] + dy < n)
        (segmento_poblacion[x_existente[j] + dx, y_existente[j] + dy] +
         entorno_empresarial[x_existente[j] + dx, y_existente[j] + dy])
);

var int: ganancia_total = ganancia_sin_nuevas + sum(i in 0..num_nuevos-1)(
    suma_segmento[i] + suma_entorno[i]
);

solve maximize ganancia_total;

% Salida
output [
    show(ganancia_sin_nuevas), "\n",  % Ganancia sin nuevas localizaciones
    show(ganancia_total), "\n",       % Ganancia con nuevas localizaciones
    % Coordenadas de localizaciones existentes, una por línea
    concat([ show(x_existente[i]) ++ " " ++ show(y_existente[i]) ++ "\n" | i in 0..num_existentes-1 ]),
    % Coordenadas de localizaciones nuevas, una por línea
    concat([ show(x_nuevo[i]) ++ " " ++ show(y_nuevo[i]) ++ "\n" | i in 0..num_nuevos-1 ])
];