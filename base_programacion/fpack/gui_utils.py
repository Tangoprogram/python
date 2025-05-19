"""
Created on 18/05/2025
@author: frposada

Herramientas para crear interfaces gráficas dinámicas con botones configurables.
Las siglas GUI significan Graphical User Interface (en español, Interfaz Gráfica de Usuario).
"""
#%%-------------------------------- Librerias ----------------------------------
import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca estandar)
from tkinter import messagebox                                                  # permite crear cuadros de dialogo (ventanas emergentes) para mostrar mensajes al usuario (biblioteca esntadar)
import tkinter.font as tkFont                                                   # permite crear constructores de fuente, es decir, definir diferentes tipos de letra (biblioteca esntadar)
import ctypes                                                                   # Proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)

#%%---------------------------- funciones y clases -----------------------------
class dynamicgui:
  """Esta clase permite la creación de una interfaz gráfica dinámica con botones configurables.

  Args:
  - header (str): Título de la ventana.
  - buttons (list): Lista de botones a crear. Cada botón debe ser un diccionario con las claves:
    * "texto": El texto que se mostrará en el botón.
    * "comando": La función que se ejecutará al presionar el botón.
  - error_handler (callable): Función que maneja errores. Si no se proporciona, se utiliza el manejador de errores por defecto.

  methods:
  - __init__(title, buttons, error_handler=None): Inicializa la interfaz gráfica.
  - _metrics(self, porcent_x, porcent_y): Método estático que permite obtener un porcentaje de la resolución del monitor.
  - _center_window(self): Método estático que centra la ventana en la pantalla.
  - _run_mainloop(self): Método estático que inicia el bucle principal de la ventana.
  - _exit_handler(self): Método estático que maneja el cierre de la ventana.
  - create_buttons(self, buttons): Crea botones dinámicamente basados en la lista de configuración proporcionada.
  - metodos(self, texto, comando): Ejecuta el comando asociado al botón presionado.
  - _default_error_handler(e): Método estático que maneja errores de forma predeterminada.

  Example:
  1. Crear una instancia de la clase con un título y una lista de botones:
    def hola_mundo():
      print("Hola mundo!")

    botones = [
      {"texto": "Decir hola", "comando": hola_mundo},
      {"texto": "Salir", "comando": lambda: print("Hasta luego!")}
    ]

    gui = DynamicGUI("Demo GUI", botones)

  2. Iniciar la interfaz gráfica:
    gui._run_mainloop()
  """
  COLORS = ["black", "white", "gray", "red", "blue", "yellow", "green", "purple", "orange", "cyan", "#C1C1C1"] # Colores
  FONT_FAMILIES = ['Arial', 'Calibri', 'Calibri Light', 'Times New Roman', 'System', 'Terminal', 'Modern', 'Roman', 'Script', 'Courier'] # Tipos de letra
  FONT_WEIGHTS = ["normal", "bold"]                                             # Grosor de la letra
  FONT_SLANTS = ["roman", "italic"]                                             # Estilo de la letra

  def __init__(self, header: str, buttons: list, error_handler: callable=None):
    """Inicializa la interfaz gráfica."""
    self.error_handler = error_handler or self._default_error_handler           # Manejador de errores por defecto
    metricas = self._metrics(1, 1)                                              # Obtiene la resolución del monitor en porcentaje

    # UI params
    self.border = 10                                                            # grosor del borde
    self.px = 10                                                                # Padding en x (espacio entre widgets)
    self.py = 10                                                                # Padding en y (espacio entre widgets)
    self.f_size = int(metricas[0])                                              # Tamaño de la fuente

    # root (Ventana raiz)
    self.root = tk.Tk()                                                         # creacion de la ventana raiz (interfaz grafica)
    self.root.title('Bancolombia')                                              # definicion del titulo de la ventana raiz
    self.root.resizable(False, False)                                           # habilita o inabilida el cambio de tamaño de la ventana en el eje X o Y

    # Fuentes
    self.font1 = tkFont.Font(family=self.FONT_FAMILIES[3],size=self.f_size,weight=self.FONT_WEIGHTS[1],slant=self.FONT_SLANTS[1]) # creacion de objeto font, donde se define el tipo de fuente a usar
    self.font2 = tkFont.Font(family=self.FONT_FAMILIES[3],size=self.f_size,weight=self.FONT_WEIGHTS[1],slant=self.FONT_SLANTS[0]) # creacion de objeto font, donde se define el tipo de fuente a usar

    # Frame principal
    self.frame = tk.Frame(self.root, bg=self.COLORS[0], bd=self.border, relief="groove") # creacion de un contenedor de widgets y personalizacion del contenedor
    self.frame.pack(side="top")                                                 # ubicacion del contenedor en la ventana raiz

    #------------------------------- widgets -----------------------------------
    # Etiqueta principal
    self.head = tk.Label(self.frame, text=header, bg=self.COLORS[0], fg=self.COLORS[8], font=self.font1) # creacion de widget tipo label
    self.head.grid(row=0, column=0, columnspan=len(buttons), padx=self.px, pady=self.py) # se crea una tabla para ubicar el widget, padx pady -> agrega un espacio entre filas y columnas

    # Creación de botones
    self.create_buttons(buttons)

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
      logging.info("La ventana fue cerrada por el usuario.")                    # Mensaje de control
      self.root.destroy()                                                       # se destruye la ventana raiz
      sys.exit()                                                                # se termina la ejecucion del script

  def create_buttons(self, buttons: list):
    """Crea botones dinámicamente basados en la lista de configuracion proporcionada.
    args:
      - buttons (list): Lista de botones a crear. Cada botón debe ser un diccionario con las claves:
        * "texto": El texto que se mostrará en el botón.
        * "comando": La función que se ejecutará al presionar el botón.
    """

    for idx, boton in enumerate(buttons):                                       # iteracion sobre la lista de botones
      b = tk.Button(self.frame, text=boton['texto'], command=lambda b=boton: self.metodos(b['texto'], b['comando']), cursor="hand2", width=15) # creacion de widget tipo boton - command -> accion al presionar el boton
      b.config(justify="center", font=self.font2, bd=self.border, relief="raised") # personalización del widget
      b.grid(row=1, column=idx, padx=self.px, pady=self.py)                     # ubicación del widget dentro de una tabla

  def metodos(self, texto: str, comando: callable):
    """Ejecuta el comando asociado al boton presionado
    args:
      - texto (str): Texto del botón presionado.
      - comando (callable): Función que se ejecutará al presionar el botón.
    """
    try:
      self.root.withdraw()                                                      # Oculta el root (ventana principal) - para que no estorbe
      logging.info(f"Iniciando ejecución de la tarea seleccionada: '{texto}'")  # mensaje de control
      comando()                                                                 # llamado a funcion
      self.root.destroy()                                                       # se destruye la ventana raiz
    except Exception as e:                                                      # en caso de excepcion
      self.root.destroy()                                                       # se destruye la ventana raiz
      self.error_handler(e)                                                     # llamado a funcion

  @staticmethod
  def _default_error_handler(e):
    """metodo estatico que maneja errores de forma predeterminada"""
    messagebox.showerror("Error", str(e))                                       # Muestra un mensaje de error
    logging.error(f"Error: {str(e)}")                                           # Mensaje de error
    sys.exit(1)                                                                 # salida del sistema con codigo 1 (0: sin errores, 1: con errores)