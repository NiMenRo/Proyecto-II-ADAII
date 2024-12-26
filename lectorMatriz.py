"""
Integrantes:
Nicolas Mauricio Rojas - 2259460
Víctor Manuel Hernandez - 2259520
Esteban Alexander Revelo - 2067507
"""

def leer_entrada(input):
    # Leer el archivo de entrada
    with open(input, 'r') as file:
        lines = file.readlines()

    # Leer el número de ubicaciones existentes
    num_existentes = int(lines[0].strip())

    # Leer las ubicaciones existentes
    ubicaciones_existentes = []
    for i in range(1, num_existentes + 1):
        x, y = map(int, lines[i].split())
        ubicaciones_existentes.append([x, y]) 

    # Leer el tamaño de la matriz
    n = int(lines[num_existentes + 1].strip())

    # Leer la matriz de segmento de población
    segmento_poblacion = []
    for line in lines[num_existentes + 2:num_existentes + 2 + n]:
        segmento_poblacion.append(list(map(int, line.strip().split())))

    # Leer la matriz de entorno empresarial
    entorno_empresarial = []
    for line in lines[num_existentes + 2 + n:num_existentes + 2 + 2 * n]:
        entorno_empresarial.append(list(map(int, line.strip().split())))

    # Leer el número de nuevas ubicaciones
    num_nuevos = int(lines[num_existentes + 2 + 2 * n].strip())

    # Devolver los datos leídos en un diccionario
    return {
        "num_existentes": num_existentes,
        "ubicaciones_existentes": ubicaciones_existentes, 
        "n": n,
        "segmento_poblacion": segmento_poblacion,
        "entorno_empresarial": entorno_empresarial,
        "num_nuevos": num_nuevos
    }
