/* 
Integrantes:
Nicolas Mauricio Rojas - 2259460
Víctor Manuel Hernandez - 2259520
Esteban Alexander Revelo - 2067507
*/

% Parámetros de entrada
int: num_existentes;
array[0..num_existentes-1, 0..1] of int: ubicaciones_existentes;
int: n;
array[0..n-1, 0..n-1] of int: segmento_poblacion;
array[0..n-1, 0..n-1] of int: entorno_empresarial;
int: num_nuevos;

array[0..num_nuevos-1, 0..1] of var 0..n-1: ubicaciones_nuevas;

% Restricciones
constraint
    % Las nuevas ubicaciones deben estar a más de 1 unidad de distancia de las existentes
    forall(new_loc in 0..num_nuevos-1, existing_loc in 0..num_existentes-1) (
        abs(ubicaciones_nuevas[new_loc, 0] - ubicaciones_existentes[existing_loc, 0]) > 1 \/
        abs(ubicaciones_nuevas[new_loc, 1] - ubicaciones_existentes[existing_loc, 1]) > 1
    );

constraint
    % Las nuevas ubicaciones deben tener al menos 25 unidades de segmento de población en su vecindad
    forall(new_loc in 0..num_nuevos-1) (
        let {
            var set of int: x_rango = max(0, ubicaciones_nuevas[new_loc, 1]-1)..min(n-1, ubicaciones_nuevas[new_loc, 1]+1),
            var set of int: y_rango = max(0, ubicaciones_nuevas[new_loc, 0]-1)..min(n-1, ubicaciones_nuevas[new_loc, 0]+1)
        } in
            sum([segmento_poblacion[i, j] | i in x_rango, j in y_rango]) >= 25
    );

constraint
    % Las nuevas ubicaciones deben tener al menos 20 unidades de entorno empresarial en su vecindad
    forall(new_loc in 0..num_nuevos-1) (
        let {
            var set of int: x_rango = max(0, ubicaciones_nuevas[new_loc, 1]-1)..min(n-1, ubicaciones_nuevas[new_loc, 1]+1),
            var set of int: y_rango = max(0, ubicaciones_nuevas[new_loc, 0]-1)..min(n-1, ubicaciones_nuevas[new_loc, 0]+1)
        } in
            sum([entorno_empresarial[i, j] | i in x_rango, j in y_rango]) >= 20
    );

constraint
    % Las nuevas ubicaciones deben estar a más de 1 unidad de distancia entre sí
    forall(i in 0..num_nuevos-1, j in 0..num_nuevos-1 where i != j) (
        abs(ubicaciones_nuevas[i, 0] - ubicaciones_nuevas[j, 0]) > 1 \/
        abs(ubicaciones_nuevas[i, 1] - ubicaciones_nuevas[j, 1]) > 1 \/
        (abs(ubicaciones_nuevas[i, 0] - ubicaciones_nuevas[j, 0]) + abs(ubicaciones_nuevas[i, 1] - ubicaciones_nuevas[j, 1]) > 1)
    );

constraint
    % Las nuevas ubicaciones no deben coincidir entre sí
    forall(i in 0..num_nuevos-1, j in 0..num_nuevos-1 where i != j) (
        ubicaciones_nuevas[i, 0] != ubicaciones_nuevas[j, 0] \/ ubicaciones_nuevas[i, 1] != ubicaciones_nuevas[j, 1]
    );

% Calcular la ganancia sin nuevas ubicaciones
int: ganancia_sin_nuevas = sum([let {
    set of int: x_rango = max(0, ubicaciones_existentes[i, 1]-1)..min(n-1, ubicaciones_existentes[i, 1]+1),
    set of int: y_rango = max(0, ubicaciones_existentes[i, 0]-1)..min(n-1, ubicaciones_existentes[i, 0]+1)
} in
    sum([segmento_poblacion[x, y] + entorno_empresarial[x, y] | x in x_rango, y in y_rango])| i in 0..num_existentes-1]);

% Calcular la ganancia total con nuevas ubicaciones
var int: ganancia_total = sum([let {
    var set of int: x_rango = max(0, ubicaciones_nuevas[i, 1]-1)..min(n-1, ubicaciones_nuevas[i, 1]+1),
    var set of int: y_rango = max(0, ubicaciones_nuevas[i, 0]-1)..min(n-1, ubicaciones_nuevas[i, 0]+1)
} in
    sum([segmento_poblacion[x, y] + entorno_empresarial[x, y] | x in x_rango, y in y_rango])| i in 0..num_nuevos-1]) + sum([let {
    set of int: x_rango = max(0, ubicaciones_existentes[i, 1]-1)..min(n-1, ubicaciones_existentes[i, 1]+1),
    set of int: y_rango = max(0, ubicaciones_existentes[i, 0]-1)..min(n-1, ubicaciones_existentes[i, 0]+1)
} in
    sum([segmento_poblacion[x, y] + entorno_empresarial[x, y] | x in x_rango, y in y_rango])| i in 0..num_existentes-1]);

% Resolver el modelo maximizando la ganancia total
solve maximize ganancia_total;

% Salida
output [
    show(ganancia_sin_nuevas), "\n",
    show(ganancia_total), "\n",
    concat([ show(ubicaciones_existentes[i, 0]) ++ " " ++ show(ubicaciones_existentes[i, 1]) ++ "\n" | i in 0..num_existentes-1 ]),
    concat([ show(ubicaciones_nuevas[i, 0]) ++ " " ++ show(ubicaciones_nuevas[i, 1]) ++ "\n" | i in 0..num_nuevos-1 ])
];