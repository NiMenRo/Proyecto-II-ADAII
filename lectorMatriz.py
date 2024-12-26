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
    for line in lines[num_existentes + 2:num_existentes + 2 + n]:
        segmento_poblacion.append(list(map(int, line.strip().split())))

    entorno_empresarial = []  
    for line in lines[num_existentes + 2 + n:num_existentes + 2 + 2 * n]:
        entorno_empresarial.append(list(map(int, line.strip().split()))) 

    num_nuevos = int(lines[num_existentes + 2 + 2 * n].strip())

    return {
        "num_existentes": num_existentes,
        "x_existente": x_existente,
        "y_existente": y_existente,
        "n": n,
        "segmento_poblacion": segmento_poblacion,
        "entorno_empresarial": entorno_empresarial,
        "num_nuevos": num_nuevos
    }
