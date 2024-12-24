def leer_entrada(ruta_archivo):
    def leer_lineas(archivo):
        with open(archivo, "r") as f:
            return f.readlines()

    def obtener_coordenadas(lineas, inicio, cantidad):
        x_coords, y_coords, coords = [], [], []
        for i in range(inicio, inicio + cantidad):
            x, y = map(int, lineas[i].strip().split())
            x_coords.append(x)
            y_coords.append(y)
            coords.append((x, y))
        return x_coords, y_coords, coords

    def obtener_matriz(lineas, inicio, filas):
        matriz = []
        for i in range(inicio, inicio + filas):
            matriz.append(list(map(int, lineas[i].strip().split())))
        return matriz

    lineas = leer_lineas(ruta_archivo)
    num_establecidos = int(lineas[0].strip())
    x_coords, y_coords, coords = obtener_coordenadas(lineas, 1, num_establecidos)
    n = int(lineas[num_establecidos + 1].strip())
    seg_poblacional = obtener_matriz(lineas, num_establecidos + 2, n)
    ent_empresarial = obtener_matriz(lineas, num_establecidos + 2 + n, n)
    num_programas = int(lineas[num_establecidos + 2 + 2 * n].strip())

    return {
        "num_establecidos": num_establecidos,
        "x_coords": x_coords,
        "y_coords": y_coords,
        "coords": coords,
        "n": n,
        "seg_poblacional": seg_poblacional,
        "ent_empresarial": ent_empresarial,
        "num_programas": num_programas
    }