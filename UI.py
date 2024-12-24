import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, StringVar, Text, Scrollbar, VERTICAL, RIGHT, Y, END
import os
from threading import Timer
from instrucciones import ejecutar_modelo

class Aplicacion(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Ingeniería al Infinito")
        self.geometry("800x600")
        
        # Variables
        self.mensaje_estado = StringVar()
        self.salida_ejecucion = None
        self.mensaje_temporal = None
        self.ruta_archivo = None
        
        self.crear_fondo()
        
        #encabezado
        encabezado = ttk.Label(self, text="Ingeniería al Infinito", font=("Comic Sans MS", 28, "bold"), anchor=CENTER)
        encabezado.pack(pady=15)
        
        self.instrucciones = ttk.Label(self, text="Por favor, selecciona tu entrada de datos", font=("Arial", 12))
        self.instrucciones.pack(pady=5)
        
        boton_archivo = ttk.Button(self, text="Seleccionar Archivo", command=self.seleccionar_archivo, bootstyle=PRIMARY)
        boton_archivo.pack(pady=10)
        
        etiqueta_estado = ttk.Label(self, textvariable=self.mensaje_estado, font=("Arial", 10))
        etiqueta_estado.pack(pady=5)
        
        # Menú desplegable y botón de ejecutar
        frame_opciones = ttk.Frame(self)
        frame_opciones.pack(pady=10)

        self.opcion_seleccionada = StringVar(value="Gecode")
        menu_opciones = ttk.Combobox(frame_opciones, textvariable=self.opcion_seleccionada, values=["Gecode", "Chuffed", "CoinBC"], state="readonly", font=("Arial", 10))
        menu_opciones.pack(side="left", padx=5)

        boton_ejecutar = ttk.Button(frame_opciones, text="▶", command=self.ejecutar, bootstyle=SUCCESS)
        boton_ejecutar.pack(side="left", padx=5)
        
        # Panel de salida
        self.crear_panel_salida()
        
        boton_guardar = ttk.Button(self, text="Guardar Salida", command=self.guardar_salida, bootstyle=PRIMARY)
        boton_guardar.pack(pady=10)

    def crear_fondo(self):
        lienzo = ttk.Canvas(self, width=800, height=600, highlightthickness=0)
        lienzo.place(x=0, y=0, relwidth=1, relheight=1)

        lienzo.create_text(100, 100, text="∞", font=("Arial", 48), fill="gray", angle=30)
        lienzo.create_text(200, 250, text="∞", font=("Arial", 35), fill="lightgray", angle=-30)
        lienzo.create_text(600, 250, text="∞", font=("Arial", 64), fill="gray", angle=20)
        lienzo.create_text(200, 400, text="∞", font=("Arial", 36), fill="lightgray", angle=15)
        lienzo.create_text(600, 150, text="∞", font=("Arial", 36), fill="lightgray", angle=-15)
        lienzo.create_text(150, 550, text="∞", font=("Arial", 36), fill="gray", angle=-35)
        lienzo.create_text(600, 550, text="∞", font=("Arial", 36), fill="lightgray", angle=-10)

    def crear_panel_salida(self):
        frame_salida = ttk.Frame(self)
        frame_salida.pack(pady=10)

        scrollbar = Scrollbar(frame_salida, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.salida_ejecucion = Text(frame_salida, wrap="word", yscrollcommand=scrollbar.set, height=10, width=60, font=("Arial", 10))
        self.salida_ejecucion.pack()
        scrollbar.config(command=self.salida_ejecucion.yview)

    def seleccionar_archivo(self):
        # Abrir explorador de archivos
        self.ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Entrada", "*.txt")])
        if self.ruta_archivo:
            if self.ruta_archivo.endswith(".txt"):
                nombre_archivo = os.path.basename(self.ruta_archivo)
                self.instrucciones.config(text=f"Archivo seleccionado: {nombre_archivo}")
            else:
                self.mensaje_estado.set("El archivo seleccionado no es válido. Por favor, selecciona un archivo .txt")

    def ejecutar(self):
        # Limpiar panel de salida
        self.salida_ejecucion.delete(1.0, END)

        if not self.ruta_archivo:
            self.mostrar_mensaje_temporal("✖ No se ha seleccionado ningún archivo", "red")
            return
        
        self.mensaje_estado.set("Ejecutando modelo...")

        opcion = self.opcion_seleccionada.get()
        if opcion == "Gecode":
            salida = ejecutar_modelo(self.ruta_archivo, "gecode")
            self.mensaje_estado.set("Ejecución con Gecode")
        elif opcion == "Chuffed":
            salida = ejecutar_modelo(self.ruta_archivo, "chuffed")
            self.mensaje_estado.set("Ejecución con Chuffed")

        elif opcion == "CoinBC":
            salida = ejecutar_modelo(self.ruta_archivo, "coinbc")
            self.mensaje_estado.set("Ejecución con CoinBC")
        else:
            salida = "Opción desconocida."    

        # Mostrar la salida en el panel
        self.salida_ejecucion.insert(END, salida + "\n")
        self.salida_ejecucion.see(END)

    def guardar_salida(self):
        # Guardar contenido del panel en un archivo .txt
        contenido = self.salida_ejecucion.get(1.0, END).strip()
        if contenido:
            archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
            if archivo:
                try:
                    with open(archivo, "w") as f:
                        f.write(contenido)
                    self.mostrar_mensaje_temporal("✔ Guardado con éxito", "green")
                except Exception as e:
                    self.mostrar_mensaje_temporal("✖ Error al guardar", "red")
            else:
                self.mostrar_mensaje_temporal("✖ Guardado cancelado", "red")
        else:
            self.mostrar_mensaje_temporal("✖ No hay contenido para guardar", "red")

    def mostrar_mensaje_temporal(self, mensaje, color):
        if self.mensaje_temporal:
            self.mensaje_temporal.destroy()

        self.mensaje_temporal = ttk.Label(self, text=mensaje, font=("Arial", 10), foreground=color)
        self.mensaje_temporal.pack(pady=5)

        Timer(3, lambda: self.mensaje_temporal.destroy()).start()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
