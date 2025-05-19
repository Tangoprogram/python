"""
Created on 23/01/2022
Plantilla
@author: frposada
"""
#%%-------------------------------- Librerias ----------------------------------
print("Importando librerías...")                                                # mensaje de control
# librerias de control
import os                                                                       # proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
import time                                                                     # para el manejo del tiempo (biblioteca estandar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
from traceback import format_exc                                                # permite extraer, formatear e imprimir el seguimiento de pila del programa (comportamiento del programa mientras se ejecuta) (biblioteca estandar)
import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca estandar)
from tkinter import messagebox                                                  # permite crear cuadros de dialogo, para informar al usuario - hay problemas con el modulo toca importarlo directamente (biblioteca estandar)
from colorama import init, Fore                                                 # facilita la impresión de texto en colores y la manipulación del estilo del texto en la terminal (No es una biblioteca estandar)

# librerias especificas

# mis librerias
import fpack                                                                    # Importa el paquete fpack y ejecuta su __init__.py para inicializar variables y funciones globales
fpack.ENABLE_DEFAULT_LOGGING = False                                            # cambiar estado de variable de control para habilitar o deshabilitar default_logging
if fpack.ENABLE_DEFAULT_LOGGING:                                                # condicion, se habilita el default_logging solo si ENABLE_DEFAULT_LOGGING es True
  fpack.default_logging()                                                       # Llama a la función default_logging para configurar el logger por defecto

from fpack.gui_utils import DynamicGUI

#%%---------------------------- Variables globales -----------------------------
print("Preparando el sistema...")                                               # mensaje de control
init(autoreset=True)                                                            # Inicializacion del modulo colorama (solo es necesario en Windows). autoreset: el estilo de color se restablecerá automáticamente después de imprimir cada línea de texto
start_time = time.time()                                                        # Guarda el tiempo inicial - para reconocer cuanto tarde el programa en ejecutarse
#! usar este cuando se ejecute el programa desde el script (archivo.py)
path_dir = "\\".join(os.path.dirname(__file__).split("\\")[: len(os.path.dirname(__file__).split("\\")) - 1]) # Ruta del directorio padre
#! usar este cuando se ejecute el programa desde el ejecutable (archivo.exe)
#path_dir = "\\".join(os.path.dirname(sys.executable).split("\\")[: len(os.path.dirname(sys.executable).split("\\")) - 1]) # Ruta del directorio padre

# LOG ..........................................................................
if not os.path.exists(path_dir + "/LOG"):                                       # condicion para verificar si la carpeta existe en la direccion especificada
  os.mkdir(path_dir + "/LOG")                                                   # si no existe la carpeta, se crea!!

if os.path.isfile(path_dir + "/LOG/Error.json"):                                # condicion para verificar si el archivo especificado existe (se elimina el archivo JSON en cada nueva ejecucion)
  os.remove(path_dir + "/LOG/Error.json")                                       # se remueve el archivo en caso de que exista

logging.basicConfig(level=20, format="[%(asctime)s] %(levelname)s: %(message)s",handlers=[logging.FileHandler(path_dir +"/LOG/Record.log", mode='w'),logging.StreamHandler(sys.stdout)]) # se establece la configuracion de los mensajes

# reading parameters ...........................................................
logging.info("Leyendo parametros...")                                           # mensaje de control

# reading inputs ...............................................................
logging.info("Leyendo insumos...")                                              # mensaje de control

# Variables ....................................................................

#%%---------------------------- funciones y clases -----------------------------
try:                                                                            # try/exception - con este par de funciones controlamos interrupciones en el programa, se ejecutara la seccion del try, en caso de que se presente una excepcion se ejecuta seccion del exception
  def errores(e):                       # Definicion de funcion (Indica como actuar en caso de que se presente un error en el programa)
    "Indica como actuar en caso de que se presente un error en el programa"
    logging.error(e)                                                            # mensaje de error
    # monstrando detalle del error
    traceback = format_exc()                                                    # permite extraer el seguimiento de pila (Ayuda a reconocer en donde se da el error)
    file = open(path_dir + "/LOG/Error.json", "w")                              # se crea y abre un archivo .json para escritura
    file.write(traceback)                                                       # se escribe en dicho archivo
    file.close()                                                                # se cierra el archivo
    # despliegue de interfaz y salida del sistema
    root = tk.Tk()                                                              # creacion de la ventana raiz (Interfaz grafica)
    tk.messagebox.showerror(message=e, title="Error!")                          # despliega mensaje de error
    root.destroy()                                                              # se destruye la ventana raiz
    sys.exit(1)                                                                 # salida del sistema con codigo 1 (0: sin errores, 1: con errores)

#-------------------------------- Main Function --------------------------------
  def main():                           # Definicion de funcion principal
    logging.info("...........")                                                 # mensaje de control

    end_time = time.time()                                                      # Guarda el tiempo final - para reconocer cuanto tarde el programa en ejecutarse
    ejecution_time = end_time - start_time                                      # calcula la duracion del programa
    logging.info("Tiempo de ejecucion: " + str(ejecution_time) + " Seg")        # mensaje de control
    logging.info("Feliz dia!!")                                                 # mensaje de control

#--------------------------------- Run program ---------------------------------
  if __name__ == "__main__":                                                    # condicion para ejecutar el programa (No ejecuta si se importa el script - puesto que este no seria el main script)
    main()                                                                      # llamado a la funcion principal del programa

except Exception as e:                                                          # en caso de excepcion
  errores(e)                                                                    # llamado a funcion

#%%---------------------------------- tests ------------------------------------