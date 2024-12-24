%
% PARAMETROS
%
int: num_ubicaciones_existentes;
array[1..num_ubicaciones_existentes] of int: x_coords; % Coordenadas x de las ubicaciones predefinidas
array[1..num_ubicaciones_existentes] of int: y_coords; % Coordenadas y de las ubicaciones predefinidas

array[1..num_ubicaciones_existentes, 1..2] of int: coords;

int: n; % Dimensión del plano
array[0..n-1,0..n-1] of int: poblacion; % Matriz de segmento de población
array[0..n-1,0..n-1]  of int: entorno; % Matriz de entorno empresarial

int: num_programas; % numero de programas


% VARIABLES
array[0..n-1,0..n-1] of var 0..1: nuevas_ubicaciones; % 1 si se selecciona, 0 si no

% INICIALIZACION
array[0..n-1,0..n-1] of int: ubicaciones_predefinidas = 
  array2d(0..n-1,0..n-1, 
        [if exists(c in 1..num_ubicaciones_existentes) 
            (i = x_coords[c] /\ j = y_coords[c]) 
            then 1 else 0 endif | i, j in 0..n-1]);

% RESTRICCIONES
constraint forall(i, j in 0..n-1)(
  ubicaciones_predefinidas[i, j] = 1 -> nuevas_ubicaciones[i, j] = 1
);

% Restricción: solo se pueden construir n nuevas_ubicaciones
constraint sum(i in 0..n-1, j in 0..n-1)(nuevas_ubicaciones[i,j]) = num_programas + num_ubicaciones_existentes;

% Restricción: no se puede construir en zonas adyacentes
constraint forall(i, j in 0..n-1)(
  nuevas_ubicaciones[i, j] = 1 -> 
  forall(k in max(0, i-1)..min(n-1, i+1), 
         l in max(0, j-1)..min(n-1, j+1))(
    % Evitar modificar la propia posición (i, j)
    (k != i \/ l != j) -> nuevas_ubicaciones[k, l] = 0
  )
);

% CALCULO DE LA SUMA DE CONTIGUOS
function int: calcular_contiguos(array[int, int] of int: matriz, int: i, int: j) = 
    sum([matriz[i + di, j + dj] | di, dj in -1..1 where (i + di >= 0 /\ i + di < n /\ j + dj >= 0 /\ j + dj < n)]);


% Restricción: Segmento poblacional >= 25 y Entorno empresarial >= 20 usando la función calcular_contiguos
constraint forall(i, j in 0..n-1)(
  nuevas_ubicaciones[i, j] = 1 -> 
  (calcular_contiguos(poblacion, i, j) >= 25 
  /\ calcular_contiguos(entorno, i, j) >= 20)
);



% Ganancia antes de la reubicación(coordenadas predefinidas)
var int: ganancia_antes = sum(x in 0..n-1, y in 0..n-1)(
    ubicaciones_predefinidas[x, y] * (poblacion[x, y] + entorno[x,y])
);

% Ganancia después de la reubicación
var int: ganancia_despues = sum(x in 0..n-1, y in 0..n-1)(
    nuevas_ubicaciones[x, y] * (poblacion[x, y] + entorno[x,y])
);

% MAXIMIZAR
solve maximize ganancia_despues;

output [
    show(ganancia_antes), "\n",
    show(ganancia_despues), "\n",
    show(nuevas_ubicaciones)
];
