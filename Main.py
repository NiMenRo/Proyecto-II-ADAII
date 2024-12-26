from minizinc import Instance, Model, Solver
from lectorMatriz import leer_entrada

def main():
    try:  
        input_file = "Entrada.txt"
        data = leer_entrada(input_file)

        model = Model("modelo.mzn")

        solver = Solver.lookup("gecode")
        instance = Instance(solver, model)

        instance["num_existentes"] = data["num_existentes"]
        instance["ubicaciones_existentes"] = data["ubicaciones_existentes"]
        instance["n"] = data["n"]
        instance["segmento_poblacion"] = data["segmento_poblacion"]
        instance["entorno_empresarial"] = data["entorno_empresarial"]
        instance["num_nuevos"] = data["num_nuevos"]

        print("Resolviendo el modelo...")
        result = instance.solve()

        print("\nContenido completo del resultado:\n")
        print(result)
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()
