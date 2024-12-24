def leer_entrada(input):
    with open(input, 'r') as file:
        lines = file.readlines()

    num_existentes = int(lines[0].strip())
    x_existente = []  
    y_existente = []  

    for i in range(1, num_existentes + 1):
        x, y = map(int, lines[i].split())
        x_existente.append(x)  
        y_existente.append(y)  

    n = int(lines[num_existentes + 1].strip())

    segmento_poblacion = []  
    for i in range(num_existentes + 2, num_existentes + 2 + n):
        row = list(map(int, lines[i].split()))
        segmento_poblacion.append(row)  

    entorno_empresarial = []  
    for i in range(num_existentes + 2 + n, num_existentes + 2 + n + n):
        row = list(map(int, lines[i].split()))
        entorno_empresarial.append(row)  

    num_nuevos = int(lines[num_existentes + 2 + n + n].strip())

    return {
        "num_existentes": num_existentes,
        "x_existente": x_existente,
        "y_existente": y_existente,
        "n": n,
        "segmento_poblacion": segmento_poblacion,
        "entorno_empresarial": entorno_empresarial,
        "num_nuevos": num_nuevos
    }
