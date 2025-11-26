"""
Created on 25/05/2025
Compilador (py to pyc)
@author: frposada
"""
#%%-------------------------------- Librerias ----------------------------------
print("Importando librerías")                                                   # mensaje de control

import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca estandar)
import tkinter.font as tkFont                                                   # permite crear constructores de fuente, es decir, definir diferentes tipos de letra (biblioteca esntadar)
from tkinter import filedialog                                                  # permite abrir un cuadro de diálogo para seleccionar archivos (biblioteca estandar)
import ctypes                                                                   # Proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
import py_compile                                                               # Permite compilar archivos de python (.py) a bytecode (.pyc) (biblioteca estandar)

#%%---------------------------- funciones y clases -----------------------------

class compiler():
  """
  Clase que permite compilar archivos de python (.py) a bytecode (.pyc)
  """
  COLORS = ["black", "white", "gray", "red", "blue", "yellow", "green", "purple", "orange", "cyan", "#C1C1C1"] # Colores
  FONT_FAMILIES = ['Segoe UI', 'Calibri', 'Arial', 'Consolas', 'Verdana']       # Tipos de letra
  FONT_WEIGHTS = ["normal", "bold"]                                             # Grosor de la letra
  FONT_SLANTS = ["roman", "italic"]                                             # Estilo de la letra

  def __init__(self):
    """Inicializa la interfaz gráfica."""
    metricas = self._metrics(1, 1)                                              # llamado a funcion

    # UI params
    self.border = 10                                                            # tamaño de los bordes
    self.px = 10                                                                # padding x
    self.py = 10                                                                # padding y
    self.f_size = max(10, int(metricas[0]))                                     # Tamaño de la fuente, asegurando que no sea menor a 12

    # root (Ventana raiz)
    self.root = tk.Tk()                                                         # creacion de la ventana raiz (interfaz grafica)
    self.root.title("Compilador Python → Bytecode")                             # definicion del titulo de la ventana raiz
    self.root.configure(bg=self.COLORS[1])
    self.root.resizable(False, False)                                           # habilita o inabilida el cambio de tamaño de la ventana en el eje X o Y

    # Fuentes
    self.font1 = tkFont.Font(family=self.FONT_FAMILIES[0], size=self.f_size, weight=self.FONT_WEIGHTS[1]) # personalizacion de la fuente
    self.font2 = tkFont.Font(family=self.FONT_FAMILIES[0], size=self.f_size, slant=self.FONT_SLANTS[1]) # personalizacion de la fuente

    # Frame principal
    self.frame = tk.Frame(self.root, bg=self.COLORS[0], bd=self.border, relief="ridge", highlightbackground=self.COLORS[6], highlightthickness=2) # creacion de un contenedor de widgets y personalizacion del contenedor
    self.frame.pack(side="top")                                                 # ubicacion del contenedor en la ventana raiz

    # ----------------------------- widgets ------------------------------------
    # Etiqueta principal
    self.head = tk.Label(self.frame, text="Compilador de Python a Bytecode", bg=self.COLORS[0], fg=self.COLORS[6], font=self.font1) # creacion de widget tipo label
    self.head.grid(row=0, column=0, padx=self.px, pady=self.py)                 # se crea una tabla para ubicar el widget, padx pady -> agrega un espacio entre filas y columnas

    # Button Compilar
    self.button = tk.Button(self.frame, text="Compilar", command=self.compilar, cursor="pirate", font=self.font2)# creacion de widget tipo boton
    self.button.config(justify="center", font=self.font1, bd=self.border, relief="raised", bg=self.COLORS[6], fg=self.COLORS[1], activebackground=self.COLORS[1], activeforeground=self.COLORS[6], width= 10) # personalizacion del widget
    self.button.grid(row=1, column=0, padx=self.px, pady=self.py)               # ubicacion del widget dentro de una tabla

  def _metrics(self, porcent_x: int, porcent_y: int):
    """metodo estatico que permite obtener un porcentaje de la resolucion del monitor
    args:
      - porcent_x (int): Porcentaje del ancho de la resolución del monitor.
      - porcent_y (int): Porcentaje de la altura de la resolución del monitor.
    Returns:
      - tuple: porcentaje de la resolución del monitor (ancho, alto).
    """
    user32 = ctypes.windll.user32                                               # se obtiene acceso a codigos (funciones) propias del sistema operativo
    user32.SetProcessDPIAware()                                                 # permite el uso de aplicaciones del escritorio de windows
    width = user32.GetSystemMetrics(0)                                          # ancho de la resolucion del monitor 'x'
    height = user32.GetSystemMetrics(1)                                         # altura de la resolucion del monitor 'y'
    return(porcent_x * width / 100, porcent_y * height / 100)                   # retorno de la funcion

  def _center_window(self):
    """metodo estatico que centra la ventana en la pantalla"""
    self.root.update_idletasks()                                                # Espera a que se cargue el contenido del root
    root_width = self.root.winfo_width()                                        # obtencion del ancho del root (el root se ajusta automaticamente al tamaño de su contenido)
    root_height = self.root.winfo_height()                                      # obtencion de la altura del root
    screen_width = self.root.winfo_screenwidth()                                # obtencion del ancho del monitor
    screen_height = self.root.winfo_screenheight()                              # obtencion de la altura del monitor
    x = int((screen_width / 2) - (root_width / 2))                              # Calculo de la posición x para centrar la ventana principal en el monitor
    y = int((screen_height / 2) - (root_height / 2))                            # Calculo de la posición y para centrar la ventana principal en el monitor
    self.root.geometry("+{}+{}".format(x, y))                                   # configuracion de la posicion del root

  def _run_mainloop(self):
    """metodo estatico que inicia el bucle principal de la ventana"""
    self.root.protocol("WM_DELETE_WINDOW", self._exit_handler)                  # asigna la funcion de cierre de la ventana
    self._center_window()                                                       # centra la ventana en la pantalla
    self.root.mainloop()                                                        # inicia el bucle principal de la ventana

  def _exit_handler(self):
    """metodo estatico que maneja el cierre de la ventana"""
    if tk.messagebox.askyesno("Salir", "Esta acción terminará la ejecución. ¿Desea continuar?"): # despliega mensaje en una nueva ventana
      print("La ventana fue cerrada por el usuario.")                           # Mensaje de control
      self.root.destroy()                                                       # se destruye la ventana raiz
      sys.exit()                                                                # se termina la ejecucion del script

  def compilar(self):
    self.root.withdraw()                                                        # Oculta el root (ventana principal)
    ruta = filedialog.askopenfilename(title="Selecciona un archivo Python", filetypes=[("Archivos Python", "*.py"), ("Todos los archivos", "*.*")])                                         # desplega una ventana de seleccion de archivo - permite al usuario seleccionar el archivo a compilar

    if not ruta:                                                                # condicion que verifica si el usuario selecciono un archivo
      print("No se seleccionó archivo")                                         # mensaje de control
      self.root.deiconify()                                                     # muestra nuevamente el root (ventana principal)
      return                                                                    # retorna a la funcion principal
    try:
      py_compile.compile(str(ruta), doraise=True)                               # Compila el archivo seleccionado. doraise=True permite que se genere una excepción si la compilación falla
      print("Compilación exitosa")                                              # mensaje de control
    except py_compile.PyCompileError as e:                                      # captura la excepcion en caso de error
      print(f"Error de compilación: {e}")                                       # mensaje de control
    finally:                                                                    # bloque que se ejecuta siempre
      print("Feliz dia!!")
      self.root.destroy()                                                       # se destruye la ventana raiz

#%%------------------------ Main Function -------------------------------------
compilador = compiler()                                                         # se crea un objeto de la clase compilador
compilador._run_mainloop()                                                      # se inicia el bucle principal de la ventana