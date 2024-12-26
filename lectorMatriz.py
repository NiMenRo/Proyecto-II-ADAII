"""
Integrantes:
Nicolas Mauricio Rojas - 2259460
Víctor Manuel Hernandez - 2259520
Esteban Alexander Revelo - 2067507
"""

def leer_entrada(input):
    
    # Abrimos el archivo de entrada en modo lectura
    with open(input, 'r') as file:
        lines = file.readlines()

    # Obtenemos el número de puntos existentes desde la primera línea
    num_existentes = int(lines[0].strip())
    x_existente = []  
    y_existente = []

    # Procesamos las coordenadas de los puntos existentes
    for i in range(1, num_existentes + 1):
        x, y = map(int, lines[i].split())
        x_existente.append(x)  
        y_existente.append(y)  

    # Leemos el número de segmentos de población
    n = int(lines[num_existentes + 1].strip())

    segmento_poblacion = []  
    # Procesamos los datos de los segmentos de población
    for line in lines[num_existentes + 2:num_existentes + 2 + n]:
        segmento_poblacion.append(list(map(int, line.strip().split())))

    entorno_empresarial = []  
    # Procesamos los datos del entorno empresarial
    for line in lines[num_existentes + 2 + n:num_existentes + 2 + 2 * n]:
        entorno_empresarial.append(list(map(int, line.strip().split()))) 

    # Leemos el número de nuevos puntos desde el archivo
    num_nuevos = int(lines[num_existentes + 2 + 2 * n].strip())

    # Retornamos un diccionario con todos los datos leídos
    return {
        "num_existentes": num_existentes,  # Número de puntos existentes
        "x_existente": x_existente,  # Coordenadas X de los puntos existentes
        "y_existente": y_existente,  # Coordenadas Y de los puntos existentes
        "n": n,  # Número de segmentos de población
        "segmento_poblacion": segmento_poblacion,  # Datos de los segmentos de población
        "entorno_empresarial": entorno_empresarial,  # Datos del entorno empresarial
        "num_nuevos": num_nuevos  # Número de nuevos puntos
    }