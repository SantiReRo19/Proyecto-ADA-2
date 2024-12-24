from minizinc import Instance, Model, Solver
from lectorArchivo import leer_entrada

def ejecutar_modelo(ruta_archivo, solverElegido):
    entrada = leer_entrada(ruta_archivo)

    num_establecidos = entrada["num_establecidos"]
    x_coords = entrada["x_coords"]
    y_coords = entrada["y_coords"]
    coords = entrada["coords"]
    n = entrada["n"]
    seg_poblacional = entrada["seg_poblacional"]
    ent_empresarial = entrada["ent_empresarial"]
    num_programas = entrada["num_programas"]

    # Cargar modelo de MiniZinc
    modelo = Model("./modelo.mzn")  # Asegúrate de que la ruta al archivo sea correcta
    solvercito = Solver.lookup(solverElegido)
    instance = Instance(solvercito, modelo)

    # Dimensión del plano y matrices
    instance["n"] = n
    instance["poblacion"] = seg_poblacional
    instance["entorno"] = ent_empresarial

    # Ubicaciones existentes
    instance["num_ubicaciones_existentes"] = num_establecidos
    instance["x_coords"] = x_coords
    instance["y_coords"] = y_coords
    instance["coords"] = coords

    # Número de programas (si se requiere)
    instance["num_programas"] = num_programas

    # Resolver el modelo
    result = instance.solve()
    print(result)

    # Resolver el modelo
    result = instance.solve()
    result_lines = str(result).splitlines()

    # Procesar la salida
    ganancia_antes = int(result_lines[0])
    ganancia_despues = int(result_lines[1])
    nuevas_ubicaciones = [int(x) for x in result_lines[2].strip('[]').split(', ')]

    # Convertir la lista de nuevas_ubicaciones a una matriz
    nuevas_ubicaciones_matriz = [nuevas_ubicaciones[i * n:(i + 1) * n] for i in range(n)]

    # Calcular las posiciones (X, Y) de las nuevas ubicaciones
    nuevas_posiciones = [(i, j) for i in range(n) for j in range(n) if nuevas_ubicaciones_matriz[i][j] == 1]

    # Transformar la salida en un string
    result_str = f"{ganancia_antes}\n"
    result_str += f"{ganancia_despues}\n"
    for pos in coords:
        result_str += f"{pos[0]} {pos[1]}\n"
    #Agregar las nuevas ubicaciones quitando las que ya existen es decir las que estan en coords
    for pos in nuevas_posiciones:
        if pos not in coords:
            result_str += f"{pos[0]} {pos[1]}\n"


    return result_str