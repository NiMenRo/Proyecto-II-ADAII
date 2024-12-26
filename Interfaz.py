"""
Integrantes:
Nicolas Mauricio Rojas - 2259460
Víctor Manuel Hernandez - 2259520
Esteban Alexander Revelo - 2067507
"""

import tkinter as tk
from tkinter import ttk, filedialog
from minizinc import Instance, Model, Solver
from lectorMatriz import leer_entrada
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz MiniZinc")
        self.root.geometry("900x900") 
        
        # Configurar colores
        self.colors = {
            'bg': '#121212',
            'text': '#E0E0E0',
            'accent': '#BB86FC',
            'highlight': '#03DAC6',
            'input_bg': '#1E1E1E',  # Fondo del Combobox
            'combobox_text': '#A0A0A0'  # Texto dentro del Combobox
        }
        
        # Configurar el tema oscuro
        self.root.configure(bg=self.colors['bg'])
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('Custom.TCombobox', 
                             fieldbackground=self.colors['text'],
                             background=self.colors['text'],
                             foreground=self.colors['bg'],
                             selectforeground=self.colors['text'],
                             selectbackground=self.colors['input_bg'])
        
        self.setup_ui()

    def setup_ui(self):
        # Crear marco principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Contenedor central
        center_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        center_frame.pack(expand=True, fill=tk.BOTH, padx=50)

        # Frame para el título y combobox
        title_frame = tk.Frame(center_frame, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, pady=(0, 20))

        # Etiqueta de selección de solver
        solver_label = tk.Label(title_frame, 
                                text="Seleccione el solucionador",
                                bg=self.colors['bg'],
                                fg=self.colors['accent'],
                                font=('Arial', 12, 'bold'))
        solver_label.pack(pady=(0, 10))

        # Frame para el combobox
        combo_frame = tk.Frame(title_frame, bg=self.colors['bg'])
        combo_frame.pack(fill=tk.X)
        
        # Combobox de solver centrado con tres opciones
        self.solver_combobox = ttk.Combobox(combo_frame, 
                                            values=["gecode", "chuffed", "coin-bc"],
                                            style='Custom.TCombobox',
                                            width=30)
        self.solver_combobox.set("gecode")
        self.solver_combobox.pack(pady=5)

        # Botón para seleccionar archivo
        file_button = tk.Button(center_frame, 
                                text="Seleccionar archivo de entrada",
                                command=self.select_file,
                                bg=self.colors['accent'],
                                fg=self.colors['text'],
                                activebackground=self.colors['highlight'],
                                activeforeground=self.colors['bg'],
                                width=30,
                                height=2,
                                relief=tk.FLAT,
                                font=('Arial', 10, 'bold'))
        file_button.pack(pady=10)

        # Frame para el estado con fondo distintivo
        status_frame = tk.Frame(center_frame, bg=self.colors['input_bg'], pady=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        # Etiqueta de estado mejorada
        self.status_label = tk.Label(status_frame, 
                                     text="Estado: Esperando archivo y solver",
                                     bg=self.colors['input_bg'],
                                     fg=self.colors['highlight'],
                                     font=('Arial', 11),
                                     pady=5)
        self.status_label.pack()

        # Botón para ejecutar
        execute_button = tk.Button(center_frame, 
                                   text="Ejecutar Modelo",
                                   command=self.run_model,
                                   bg=self.colors['accent'],
                                   fg=self.colors['text'],
                                   activebackground=self.colors['highlight'],
                                   activeforeground=self.colors['bg'],
                                   width=30,
                                   height=2,
                                   relief=tk.FLAT,
                                   font=('Arial', 10, 'bold'))
        execute_button.pack(pady=10)

        # Área de texto para resultados con marco
        result_frame = tk.Frame(center_frame, 
                                 bg=self.colors['accent'],
                                 padx=2, 
                                 pady=2)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, 
                                   height=12,  # Aumentado el tamaño
                                   bg=self.colors['input_bg'],
                                   fg=self.colors['text'],
                                   insertbackground=self.colors['text'],
                                   font=('Consolas', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Configurar el estilo del gráfico
        plt.style.use('dark_background')
        self.figure = plt.Figure(figsize=(6, 5), dpi=100, facecolor=self.colors['bg'])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(self.colors['bg'])
        self.canvas = FigureCanvasTkAgg(self.figure, master=center_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, pady=10)

        self.input_file = None

    def select_file(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo
        self.input_file = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if self.input_file:
            self.status_label.config(text=f"Archivo seleccionado: {self.input_file}")
        else:
            self.status_label.config(text="No se seleccionó ningún archivo")

    def run_model(self):
        # Verificar si se ha seleccionado un archivo
        if not self.input_file:
            self.status_label.config(text="Por favor, seleccione un archivo de entrada primero.")
            return

        solver_name = self.solver_combobox.get()
        self.status_label.config(text="Resolviendo el modelo...")
        self.root.update_idletasks()

        try:
            # Leer los datos del archivo de entrada
            data = leer_entrada(self.input_file)

            # Configurar el modelo y el solver
            model = Model("modelo.mzn")
            solver = Solver.lookup(solver_name)
            instance = Instance(solver, model)

            # Asignar datos a la instancia del modelo
            instance["num_existentes"] = data["num_existentes"]
            instance["ubicaciones_existentes"] = data["ubicaciones_existentes"]
            instance["n"] = data["n"]
            instance["segmento_poblacion"] = data["segmento_poblacion"]
            instance["entorno_empresarial"] = data["entorno_empresarial"]
            instance["num_nuevos"] = data["num_nuevos"]

            # Resolver el modelo
            result = instance.solve()

            # Guardar el resultado en un archivo de texto
            with open("resultado.txt", "w") as result_file:
                result_file.write(str(result))

            # Mostrar los resultados
            self.display_result(result, data)
            self.status_label.config(text="Modelo resuelto con éxito. Resultado guardado en 'resultado.txt'.")

        except Exception as e:
            self.status_label.config(text=f"Error durante la ejecución: {e}")

    def display_result(self, result, data):
        # Limpiar el área de texto de resultados
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result))

        # Configurar y mostrar el gráfico de resultados
        self.ax.clear()
        n = data["n"]
        self.ax.set_xlim(0, n + 1)
        self.ax.set_ylim(0, n + 1)
        self.ax.set_title("Ubicaciones propuestas", color=self.colors['text'], pad=20, fontsize=12)
        self.ax.set_xlabel("X", color=self.colors['text'], fontsize=10)
        self.ax.set_ylabel("Y", color=self.colors['text'], fontsize=10)
        
        self.ax.tick_params(colors=self.colors['text'])
        self.ax.spines['bottom'].set_color(self.colors['text'])
        self.ax.spines['top'].set_color(self.colors['text'])
        self.ax.spines['left'].set_color(self.colors['text'])
        self.ax.spines['right'].set_color(self.colors['text'])

        # Dibujar puntos existentes y nuevos en el gráfico
        ubicaciones_existentes = data["ubicaciones_existentes"]
        self.ax.scatter(ubicaciones_existentes, c=self.colors['accent'], label="Existentes", s=100)

        x_nuevo = [int(var) for var in result["x_nuevo"]]
        y_nuevo = [int(var) for var in result["y_nuevo"]]
        self.ax.scatter(x_nuevo, y_nuevo, c=self.colors['highlight'], label="Nuevos", s=100)

        self.ax.legend(facecolor=self.colors['bg'], labelcolor=self.colors['text'])
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()