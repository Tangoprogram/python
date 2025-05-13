"""
Created on Fri Sep 16 10:05:53 2022
Funciones basicas
@author: frposada
"""
import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
import os                                                                       # proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
import getpass                                                                  # proporciona una forma segura de manejar las solicitudes de contraseña donde los programas interactúan con los usuarios a través de la terminal (biblioteca estandar)
import shutil                                                                   # permite la copia y remoción de archivos (biblioteca estandar)
import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca estandar)
from tkinter import filedialog                                                  # proporciona un cuadro de diálogo de archivo para que el usuario seleccione un directorio (biblioteca estandar)

#%%-------------------------- funciones y clases -------------------------------

#input("press enter") # para detener la ejecucion del codigo

def block(contraseña):                  # Definicion de funcion (bloquea el script, es decir, sin clave no se continua la ejecucion)
  logging.info("Validacion de permisos...")                                     # mensaje de control
  password = 0                                                                  # inicializacion de variable
  intentos = 0                                                                  # inicializacion de variable

  while password != contraseña:                                                 # ciclo numero de intentos para ingresar la contraseña
    if intentos == 2:                                                           # condicion para mensaje de advertencia
      logging.info("Ultimo intento...")                                         # mensaje de control
    elif intentos == 3:                                                         # condicion para terminar la ejecucion del programa
      logging.info("Acceso denegado...")                                        # mensaje de control
      sys.exit()                                                                # salida del programa

    password = getpass.getpass("Contraseña: ")                                  # se le solicita al usuario la contraseña
    intentos += 1                                                               # aumento del contador
  logging.info("Acceso concedido...")                                           # mensaje de control
  """
  contraseña: como su nombre lo indica es la contraseña que se destinara como requisito para permitir la ejecucion del programa
  """

def create_folder(path_dir,name):       # Definicion de funcion (crea carpeta en el Directorio donde se ejecuta el script de Python)
  if not os.path.exists(path_dir + "/"+ name):                                  # condicion para verificar si la carpeta existe en la direccion especificada
    os.mkdir(path_dir + "/" + name)                                             # si no existe la carpeta, se crea!!
  """
  Path_dir: ruta donde se desea crear la carpeta
  name: nombre de la carpeta
  """

def create_file(path_dir,name,extension,content): # Definicion de funcion (crea un archivo con la extension que se le suministre y almacena informacion en el)
  file = open(path_dir + "/" + name + extension, "w")                           # se crea y abre un archivo con la extension especificada para escritura
  file.write(str(content))                                                      # se escribe en dicho archivo
  file.close()                                                                  # se cierra el archivo
  """
  Path_dir: ruta donde se desea guardar el archivo
  name: nombre del archivo
  extension: extension (EJ: .txt  .py .log   etc) - debe anteponer el "."
  content: contenido del archivo, lo que se desea escribir en el
  """

def remove_Files(path_dir):             # Definicion de funcion (Elimina los archivos dentro de la carpeta seleccionada)
  for f in os.listdir(path_dir):                                                # ciclo para recorrer todos los elementos de la carpeta
    os.remove(path_dir + "/" + f)                                               # se remueven los elementos de la carpeta
  """
  Path_dir: ruta de la carpeta
  """

def copy_paste_file(file_dir, folder_dir, file): # Definicion de funcion (define la ruta (carpeta) donde se depositara la copia del archivo seleccionado)
  file_path = file_dir + "/" + file                                             # definicion de la ruta donde esta el archivo a copiar

  if not os.path.isfile(folder_dir + "/Path.txt"):                              # condicion para verificar si no existe el archivo
    save_folder_dir(folder_dir)                                                 # llamado a funcion - creacion del archivo path en donde se especifica la ruta de la donde se depositara el archivo seleccionado

  archivo = open(folder_dir + "/Path.txt")                                      # se abre el archivo especificado
  new_file_path = archivo.read()                                                # Leectura del archivo donde se especifica la ruta en la que se copiara el archivo
  logging.info(new_file_path)                                                   # mensaje de control
  new_file_path = new_file_path + "/" + file                                    # define la nueva ruta del archivo
  if not os.path.isfile(new_file_path):                                         # condicion para verificar si no existe el archivo en la carpeta especificada
    shutil.copy(file_path, new_file_path)                                       # copia del archivo en la nueva ruta
  return (new_file_path)                                                        # retorno de funcion
  """
  Importante - es necesario crear la carpeta que se especifique en el "folder_dir" antes de usar esta funcion
  file_dir: define la ruta donde se encuentra el archivo que se desea copiar
  folder_dir: define la ruta donde se puede encontrar el archivo txt donde se especifica la ruta de donde se depositara la copia del archivo seleccionado
  file: define el archivo a copiar (es necesario pasar el nombre del archivo con su extension)
  """

def save_folder_dir(path_dir):          # Definicion de funcion (crea un archivo txt con la ruta de la carpeta que se seleccione)
  if not os.path.isfile(path_dir + "/Path.txt"):                                # condicion para verificar si no existe el archivo
    #--------------------- creacion interfaz de usuario ------------------------
    root = tk.Tk()                                                              # creacion de la ventana raiz (interfaz grafica)
    root.title("Selecionar carpeta")                                            # definicion del titulo de la ventana raiz
    root.resizable(False, False)                                                # habilita o inabilida el cambio de tamaño de la ventana en el eje X o Y
    #------------------- frame (contenedor de los widgets) ---------------------
    frame = tk.Frame(root, bg="gray")                                           # Creacion del frame
    frame.pack()                                                                # se empaqueta el frame dentro de la ventana raiz creada
    frame.config(bd = 10)                                                       # define un tamaño de borde
    frame.config(relief = "sunken")                                             # define el tipo de borde
    #------------------------------- widgets -----------------------------------
    label = tk.Label(frame, text="Selecione la carpeta en que desea guardar el archivo") # creacion de label
    label.grid(row=0, column=0, sticky="w", padx="10", pady="5")                # ubicacion del widget dentro de una tabla
    label.config(fg="white", bg="gray", font=("Verdana","20"))                  # personalizacion del widget
    #---------------------------------------------------------------------------
    out_askdirectory = True                                                     # se crea variable booleana usada como bandera (por defecto en True)
    while out_askdirectory:                                                     # ciclo mientras se cumpla condicion
      filePath = tk.filedialog.askdirectory(initialdir = "C:/Users/" + str((getpass.getuser()))) # desplega una ventana de seleccion de carpeta - permite al usuario seleccionar la carpeta donde se almacenara el archivo
      if filePath != "":                                                        # condicion para verificar que se ha seleccionado una carpeta
        out_askdirectory = False                                                # cambio del estado de la bandera
    root.destroy()                                                              # destruye la interfaz

    file = open(path_dir + "/Path.txt", "w")                                    # se abre el archivo especificado para escritura
    file.write(str(filePath))                                                   # se escribe en el archivo la ruta de la carpeta elegida
    file.close()                                                                # se cierra el archivo
  else:
    logging.info("Ya existe el archivo")                                        # mensaje de control
  """
  Path_dir: define la ruta donde se guardara el txt con la ruta de la carpeta seleccionada
  """