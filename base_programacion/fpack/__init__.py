"""
Created on 18/05/2025
@author: frposada

FPack: paquete de utilidades para la automatización de procesos y manejo de datos.

Módulos:
--------
- file_utils: Funciones para manejo de archivos y datos, incluyendo protección de archivos Excel.
- gui_utils: Herramientas para crear interfaces gráficas dinámicas con botones configurables.
- security_utils: Funciones para manejo seguro de credenciales y bloqueo de scripts por contraseña.
- external_utils: Utilidades externas y soporte para integración con otras bibliotecas.
"""
#%%-------------------------------- Librerias ----------------------------------
import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)

#%%---------------------------- Variables globales -----------------------------
APP_NAME = "FPack Utilities"
VERSION = "1.0.0"

ENABLE_DEFAULT_LOGGING = False                                                  # Variable de control para habilitar o deshabilitar default_logging

#%%---------------------------- funciones y clases -----------------------------
def default_logging():
  """
  Configura un logger por defecto si no hay un logger global configurado.

  - El logger por defecto envía los mensajes al stdout.
  - El formato incluye el nivel de log y el mensaje.
  """
  root_logger = logging.getLogger()                                             # Obtiene el logger raíz (global) (objeto utilizado para registrar eventos y mensajes de log)
  if not root_logger.hasHandlers():                                             # Verifica si el logger raíz ya tiene manejadores configurados, es decir, si se heredó la configuración global del script principal.
    handler = logging.StreamHandler(sys.stdout)                                 # establece un manejador que envía los mensajes a la salida estándar (consola)
    handler.setLevel(20)                                                        # Establece el nivel de log para el manejador
    formatter = logging.Formatter("%(message)s")                                # establece el formato de los mensajes de log
    handler.setFormatter(formatter)                                             # Aplica el formato al manejador
    root_logger.addHandler(handler)                                             # Agrega el manejador al logger
    root_logger.setLevel(20)                                                    # Establece el nivel de log para el logger

#------------------------------------ Main -------------------------------------
if ENABLE_DEFAULT_LOGGING:                                                      # condicion, se habilita el default_logging solo si ENABLE_DEFAULT_LOGGING es True
  default_logging()                                                             # Llama a la función default_logging para configurar el logger por defecto

#%%-------------------------- librerias del paquete  ---------------------------
# import os                                                                       # proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
# import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
# import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
# import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca estandar)
# from tkinter import messagebox                                                  # permite crear cuadros de dialogo (ventanas emergentes) para mostrar mensajes al usuario (biblioteca esntadar)
# import tkinter.font as tkFont                                                   # permite crear constructores de fuente, es decir, definir diferentes tipos de letra (biblioteca esntadar)
# import ctypes                                                                   # Proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
# import getpass                                                                  # permite solicitar al usuario que ingrese información sensible (como contraseñas) desde la terminal sin mostrar lo que escribe en pantalla (biblioteca estandar)
# import base64                                                                   # Proporciona funciones para codificar y decodificar datos en formato base64 (biblioteca estandar)

# import pandas as pd                                                             # para el manejo y analisis de estructuras de datos
# from openpyxl import load_workbook                                              # para leer y escribir archivos de Excel
# from openpyxl.styles import Protection                                          # para aplicar estilos a las celdas de Excel

# from cryptography.hazmat.backends import default_backend                        # Proporciona una interfaz para trabajar con algoritmos criptográficos
# from cryptography.hazmat.primitives import hashes                               # Proporciona funciones para trabajar con algoritmos de hash
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC                # Proporciona una implementación del algoritmo PBKDF2 (Password-Based Key Derivation Function 2)
# from cryptography.fernet import Fernet                                          # Proporciona una implementación del cifrado simétrico Fernet
# import keyring                                                                  # Proporciona una interfaz para almacenar y recuperar credenciales de forma segura

# from selenium.webdriver.support import expected_conditions as EC                # este modulo permite realizar las esperas explicitas, es decir el programa espera hasta que se cumpla la condicion
# from selenium.webdriver.common.by import By                                     # este modulo permite identificar objetos por (by) un atributo especifico del elemento como: name, id, etc (Se usa principalmente para los explicit wait)
# import win32com.client as win32                                                 # permite interactuar con objetos COM y automatizar aplicaciones de Windows
