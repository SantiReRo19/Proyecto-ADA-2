% Parámetros
int: n; % Dimensión del plano

array[1..n, 1..n] of int: poblacion; % Matriz de segmento de población
array[1..n, 1..n] of int: entorno; % Matriz de entorno empresarial
int: num_ubicaciones_existentes;
array[1..num_ubicaciones_existentes, 1..2] of int: ubicaciones_existentes; % Coordenadas de las ubicaciones existentes 

%int: num_programas; % numero de programas

% Variables
array[1..n, 1..n] of var 0..1: nuevas_ubicaciones; % 1 si se selecciona, 0 si no

% Inicialización de las nuevas_ubicaciones predefinidas con intercambio de coordenadas
%array[1..n, 1..n] of int: ubicaciones_pre = 
%  array2d(1..n, 1..n, 
%    [if exists(c in 1..num_ubicaciones_existentes) 
%        (i = ubicaciones_existentes[c, 2] /\ j = ubicaciones_existentes[c, 1]) 
%     then 1 else 0 endif | i, j in 1..n]);


% Restricción: las nuevas_ubicaciones predefinidas deben permanecer como 1
constraint forall(i, j in 1..n)(
  ubicaciones_existentes[i, j] = 1 -> nuevas_ubicaciones[i, j] = 1
);


% Restricción: solo se pueden construir n nuevas_ubicaciones
%constraint sum(i in 1..n, j in 1..n)(nuevas_ubicaciones[i,j]) = num_programas + num_ubicaciones_existentes;

% Restricciones
constraint forall(x in 1..n, y in 1..n)(
    if nuevas_ubicaciones[x, y] = 1 then
        % Restricción de contigüidad: no puede estar junto a las nuevas_ubicaciones existentes
        forall(dx, dy in {-1, 0, 1} where dx != 0 \/ dy != 0)(
            let {int: nx = x + dx, int: ny = y + dy} in
            nx > 0 /\ ny > 0 /\ nx <= n /\ ny <= n ->
            poblacion[nx, ny] + entorno[nx, ny] >= 25
        )
    else true
    endif
);

% Maximizar
solve maximize sum(x in 1..n, y in 1..n)(
    nuevas_ubicaciones[x, y] * (poblacion[x, y] + entorno[x,y])
);