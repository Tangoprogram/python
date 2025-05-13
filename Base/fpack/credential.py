"""
Created on Fri Sep 16 17:03:30 2022
Credenciales (Usuario y contraseña)
@author: frposada
"""
import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca esntadar)
import os                                                                       # proporciona funciones para interactuar con el sistema operativo (biblioteca esntadar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca esntadar)
import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca esntadar)
from tkinter import messagebox                                                  # permite crear cuadros de dialogo, para informar al usuario - hay problemas con el modulo toca importarlo directamente (biblioteca esntadar)
import tkinter.font as tkFont                                                   # permite crear constructores de fuente, es decir, definir diferentes tipos de letra (biblioteca esntadar)
import json                                                                     # permite trabajar con datos Json (biblioteca estandar)
import base64                                                                   # proporciona funciones para codificar datos binarios en caracteres ASCII imprimibles y decodificar dichas codificaciones en datos binarios. (biblioteca esntadar)
from getpass import getuser                                                     # proporciona una forma segura de manejar las solicitudes de contraseña donde los programas interactúan con los usuarios a través de la terminal (biblioteca esntadar)

#%%-------------------------- funciones y clases -------------------------------
def write_credentials(path_dir,name):   # Definicion de funcion (verifica si existe el archivo JSON con las credenciales, si no existe lo crea)
  if not os.path.isfile(path_dir +"/"+ name + ".json"):                         # condicion para verificar si no existe el archivo Json
    logging.info("Actualizando credenciales...")                                # Mensaje de control
    obj = i_grafica(name)                                                       # creacion del objeto de clase I_grafica
    jsonData = (obj.credentials[1], obj.credentials[0])                         # creacion de diccionario para almacenar usuario y clave
    with open(path_dir +"/"+ name + ".json", "w") as file:                      # se abre el archivo especificado para escritura
      json.dump(jsonData, file)                                                 # con dump se convierte los objetos de Python en objetos json apropiados
  """
  path_dir: ruta donde se desea crear el archivo json
  name: nombre del aplicativo al que pertenecen las credenciales
  """

class i_grafica:                        # Creacion de la clase objeto interfaz grafica
  def __init__(self,name):              # Definicion de la clase
    #----------------------- root (Ventana raiz)--------------------------------
    self.root = tk.Tk()                                                         # creacion de la ventana raiz (interfaz grafica)
    self.root.title('Credenciales')                                             # definicion del titulo de la ventana raiz
    self.root.resizable(False, False)                                           # habilita o inabilida el cambio de tamaño de la ventana en el eje X o Y

    #...................... Parametros de la interfaz ..........................
    screen_width = self.root.winfo_screenwidth()                                # obtencion del ancho del monitor
    screen_height = self.root.winfo_screenheight()                              # obtencion de la altura del monitor
    x_porcent = 1                                                               # porcentaje en el ancho
    y_porcent = 1                                                               # porcentaje en la altura
    metricas = [x_porcent * screen_width / 100, y_porcent * screen_height / 100]# porcentaje del ancho y la altura de la resolucion del monitor

    color = ["black","white","gray","red","blue","yellow","green","purple","orange","cyan","#C1C1C1"] # lista de colores
    px = 5                                                                      # padding x
    py = 5                                                                      # padding y
    border = 5                                                                  # tamaño de los bordes

    # parametros de las fuentes (tipos de letras)
    f_family = ['Arial','Calibri','Calibri Light','Times New Roman','System','Terminal','Modern','Roman','Script','Courier'] # familia de fuentes - algunos ejemplos
    f_size = int(metricas[0])                                                   # tamaño de la fuente en puntos (pixeles)
    f_weight = ["normal","bold"]                                                # espesor
    f_slant = ["roman", "italic"]                                               # inclinación de la fuente

    #..................... constructor de las fuentes ..........................
    font1 = tkFont.Font(family=f_family[1],size=f_size,weight=f_weight[1],slant=f_slant[0]) # creacion de objeto font, donde se define el tipo de fuente a usar
    font2 = tkFont.Font(family=f_family[1],size=f_size,weight=f_weight[0],slant=f_slant[0]) # creacion de objeto font, donde se define el tipo de fuente a usar

    #----------------- frame (contenedor de los widgets) -----------------------
    self.frame = tk.Frame(self.root, bg=color[0])                               # Creacion del frame
    self.frame.pack(side="top")                                                 # se empaqueta el frame dentro de la ventana raiz creada y se especifica su posicion
    self.frame.config(bd=border, relief="groove")                               # define un tamaño y tipo de borde

    #------------------------------- widgets -----------------------------------
    # Label de titulo
    self.tittle = tk.Label(self.frame, text='Credenciales de ' + name)          # creacion de widget tipo label
    self.tittle.grid(row=0, column=0,columnspan=2, padx=px, pady=py)            # se crea una tabla para ubicar el widget
    self.tittle.config(bg=color[0], fg=color[8], font=font1)                    # personalizacion del widget

    # Label identificacion usuario (UID)
    self.UID_label = tk.Label(self.frame, text="USUARIO:")                      # creacion de label
    self.UID_label.grid(row=1, column=0, sticky="w", padx=px, pady=py)          # se crea una tabla para ubicar el widget, sticky="w" -> ancla la tabla al lado izquierdo del frame, padx pady -> agrega un espacio entre filas y columnas
    self.UID_label.config(bg=color[0], fg=color[1], font=font1)                 # personalizacion del widget
    # TextBox identificacion usuario (UID)
    self.UID = tk.StringVar()                                                   # definicion de variable tipo string
    self.textBoxUID = tk.Entry(self.frame, textvariable=self.UID)               # creacion de widget de entrada de texto por usuario
    self.textBoxUID.config(justify="left", font=font2, width="20")              # personalizacion del widget
    self.textBoxUID.grid(row=1, column=1, sticky="w", padx=px, pady=py)         # ubicacion del widget dentro de una tabla
    self.UID.set(str(getuser()))                                                # establece el valor de la variable UID, haciendo uso de la funcion getpass.getuser() - trae el usuario del pc, para ahorrar tiempo en el requerimiento de pedir el usuario
    # Label contraseña usuario (PASS)
    self.PASS_label = tk.Label(self.frame, text="CONTRASEÑA:")                  # creacion de label
    self.PASS_label.grid(row=2, column=0, sticky="w", padx=px, pady=py)         # ubicacion del widget dentro de una tabla
    self.PASS_label.config(bg=color[0], fg=color[1], font=font1)                # personalizacion del widget
    # TextBox contraseña usuario (PASS)
    self.PASS = tk.StringVar()                                                  # definicion de variable tipo string
    self.textBoxPASS = tk.Entry(self.frame, textvariable=self.PASS, show="*")   # creacion de widget de entrada de texto por usuario
    self.textBoxPASS.config(justify="left", font=font2, width="20")             # personalizacion del widget
    self.textBoxPASS.grid(row=2, column=1, sticky="w", padx=px, pady=py)        # ubicacion del widget dentro de una tabla

    # Button Aceptar
    self.boton = tk.Button(self.frame, text="ACEPTAR", command=self.Aceptar, cursor="hand2") # creacion de widget tipo boton
    self.boton.config(justify="center", font=font1, bd=border, relief='raised') # personalizacion del widget
    self.boton.grid(row=4, column=0, columnspan=2, padx=px, pady=py)            # ubicacion del widget dentro de una tabla

    #....................... Ubicacion del root ..............................
    self.root.update_idletasks()                                                # Espera a que se cargue el contenido del root
    root_width = self.root.winfo_width()                                        # obtencion del ancho del root (el root se ajusta automaticamente al tamaño de su contenido)
    root_height = self.root.winfo_height()                                      # obtencion de la altura del root
    x = int((screen_width / 2) - (root_width / 2))                              # Calculo de la posición x para centrar la ventana principal en el monitor
    y = int((screen_height / 2) - (root_height / 2))                            # Calculo de la posición y para centrar la ventana principal en el monitor
    self.root.geometry("+{}+{}".format(x, y))                                   # configuracion de la posicion del root
    #.........................................................................

    self.textBoxPASS.focus_set()                                                # Al iniciar se centra el cursor en el widget especificado
    self.root.protocol("WM_DELETE_WINDOW", self.on_exit)                        # En caso de intentar cerrar la ventana se ejecuta la funcion on_exit (funcion de seguridad para no cerrar la ventana)
    self.root.mainloop()                                                        # Bucle infinito para que la ventana se mantenga desplegada (debe estar al final de la clase)

  #--------------------------- Funciones internas ------------------------------
  def on_exit(self):                    # Definicion de funcion interna (sistema de seguridad para evitar cerrar la ventana)
    if tk.messagebox.askyesno("Salir", "Esta acción terminará la ejecución de la EUC ¿Desea continuar?"): # despliega mensaje en una nueva ventana
      self.root.destroy()                                                       # se destruye la ventana raiz
      sys.exit()                                                                # salida del sistema

  def Aceptar(self):                    # Definicion de funcion interna (define q ocurre al precionar el boton aceptar)
    N_UID = self.UID.get()                                                      # obtiene el valor de la variable
    N_PASS = self.PASS.get()                                                    # obtiene el valor de la variable
    if (N_UID == ""):                                                           # condicion para verificar que la variable no este vacia
      tk.messagebox.showerror("¡Error!", "Campo USUARIO no puede estar vacío.") # despliegue de mensaje en nueva ventana
    elif (N_PASS == ""):                                                        # condicion para verificar que la variable no este vacia
      tk.messagebox.showerror("¡Error!", "Campo CONTRASEÑA no puede estar vacío.") # despliegue de mensaje en nueva ventana
    else:                                                                       # en caso que no esten vacios
      self.UID.set("")                                                          # reinicio de la variable del objeto
      self.PASS.set("")                                                         # reinicio de la variable del objeto
      self.credentials = ((base64.b64encode(N_UID.encode("utf-8"))).decode("utf-8"), (base64.b64encode(N_PASS.encode("utf-8"))).decode("utf-8")) # Codifica la informacion para que no sea reconocible (Puesto que estas se guardaran en el archivo json visible por los ususarios)
      self.root.destroy()                                                       # destruye la ventana
  #* name: nombre del aplicativo al que pertenecen las credenciales

def read_credentials(path_dir,name):    # Definicion de funcion (Lee las credenciales de acceso)
  with open(path_dir +"/"+ name + ".json","r") as file:                       # se abre el archivo especificado para lectura
    credentials = json.load(file)                                             # se cargan las credenciales
  conn = {'UID': base64.b64decode(credentials[1]).decode("utf-8"), 'PWD': base64.b64decode(credentials[0]).decode("utf-8")}
  return (conn)                                                               # retorno de la funcion
  """
  Path_dir: ruta donde se esta el archivo json
  Name: nombre de las credenciales
  """
