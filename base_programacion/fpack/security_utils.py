"""
Created on 18/05/2025
@author: frposada

Funciones para manejo seguro de credenciales y bloqueo de scripts por contraseña.
"""
#%%-------------------------------- Librerias ----------------------------------
import os                                                                       # proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
import sys                                                                      # para manipular diferentes partes del entorno de tiempo de ejecución (biblioteca estandar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
import tkinter as tk                                                            # Proporciona una interfaz gráfica de usuario (biblioteca estandar)
from tkinter import messagebox                                                  # permite crear cuadros de dialogo (ventanas emergentes) para mostrar mensajes al usuario (biblioteca esntadar)
import tkinter.font as tkFont                                                   # permite crear constructores de fuente, es decir, definir diferentes tipos de letra (biblioteca esntadar)
import ctypes                                                                   # Proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
import getpass                                                                  # permite solicitar al usuario que ingrese información sensible (como contraseñas) desde la terminal sin mostrar lo que escribe en pantalla (biblioteca estandar)
import base64                                                                   # Proporciona funciones para codificar y decodificar datos en formato base64 (biblioteca estandar)

from cryptography.hazmat.backends import default_backend                        # Proporciona una interfaz para trabajar con algoritmos criptográficos
from cryptography.hazmat.primitives import hashes                               # Proporciona funciones para trabajar con algoritmos de hash
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC                # Proporciona una implementación del algoritmo PBKDF2 (Password-Based Key Derivation Function 2)
from cryptography.fernet import Fernet                                          # Proporciona una implementación del cifrado simétrico Fernet
import keyring                                                                  # Proporciona una interfaz para almacenar y recuperar credenciales de forma segura

#%%---------------------------- funciones y clases -----------------------------
def block(contraseña: str, max_attempts: int = 3):
  """Bloquea la ejecución del script hasta que se ingrese la contraseña correcta.

  Args:
    - contraseña (str): Contraseña que se debe ingresar para desbloquear el script.
    - max_attempts (int, optional): Número máximo de intentos permitidos. Default: 3.

  Raises:
    PermissionError: Si se excede el número máximo de intentos.

  Example:
    block("mi_contraseña", max_attempts=3)
  """
  messages = {                                                                  # Mensajes predeterminados
    "validation": "Validación de permisos...",
    "last_attempt": "Último intento...",
    "access_denied": "Acceso denegado...",
    "access_granted": "Acceso concedido...",
    "prompt": "Contraseña: "
  }

  logging.info(messages["validation"])                                          # Mensaje de inicio de validación
  password = 0                                                                  # inicializacion de variable
  intentos = 0                                                                  # inicializacion de variable

  while password != contraseña:                                                 # ciclo numero de intentos para ingresar la contraseña
    if intentos == max_attempts - 1:
      logging.info(messages["last_attempt"])                                    # Mensaje de último intento
    elif intentos == max_attempts:
      logging.info(messages["access_denied"])                                   # Acceso denegado
      sys.exit()                                                                # salida del programa

    password = getpass.getpass(messages["prompt"])                              # se le solicita al usuario la contraseña
    intentos += 1                                                               # aumento del contador
  logging.info(messages["acceso concedido"])                                    # Acceso concedido

class credentialmanager:
  """
  clase que gestiona las credenciales de forma segura.
  Esta clase permite guardar y recuperar credenciales cifradas mediante una interfaz gráfica basada en `tkinter`.
  Las credenciales se almacenan de forma segura en el sistema utilizando `keyring` y se cifran con `Fernet`.
  En windows, valida la creacion de credenciales en el administrador de credenciales de windows.

  Args:
  - service (str): Nombre del servicio para el que se gestionan las credenciales.
  - error_handler (callable): Función que maneja errores. Si no se proporciona, se utiliza el manejador de errores por defecto.

  methods:
  - _init__(self, service, error_handler=None): Inicializa el gestor de credenciales.
  - _metrics(self, porcent_x, porcent_y): Método estático que permite obtener un porcentaje de la resolución del monitor.
  - _center_window(self): Método estático que centra la ventana en la pantalla.
  - _setup_fonts(self): Método estático que configura las fuentes para la interfaz gráfica.
  - _build_frame(self, title): Método estático que construye el marco principal de la interfaz gráfica.
  - _create_labeled_entry(self, label_text, variable, row, show=None, focal=False): Método estático que crea un campo de entrada con etiqueta.
  - _run_mainloop(self): Método estático que inicia el bucle principal de la ventana.
  - _exit_handler(self): Método estático que maneja el cierre de la ventana.
  - gui_save(self): Crea la interfaz gráfica para guardar las credenciales.
  - gui_load(self): Crea la interfaz gráfica para cargar las credenciales.
  - _derive_key(self, key, salt): Método estático que deriva una clave binaria segura desde una llave usando PBKDF2-HMAC-SHA256.
  - save(self): Guarda las credenciales cifradas en el almacén seguro del sistema.
  - load(self): Carga las credenciales cifradas del almacén seguro del sistema.
  - _default_error_handler(e): Método estático que maneja errores de forma predeterminada.

  example:
  1. Crear una instancia de `CredentialManager` pasando el nombre del servicio.
    manager = CredentialManager("servicio")
  2. Llamar a `gui_save()` para guardar las credenciales.
    manager.gui_save()
  3. Llamar a `gui_load()` para cargar las credenciales.
    manager.gui_load()
  """
  COLORS = ["black", "white", "gray", "red", "blue", "yellow", "green", "purple", "orange", "cyan", "#C1C1C1"] # Colores
  FONT_FAMILIES = ['Arial', 'Calibri', 'Calibri Light', 'Times New Roman', 'System', 'Terminal', 'Modern', 'Roman', 'Script', 'Courier'] # Tipos de letra
  FONT_WEIGHTS = ["normal", "bold"]                                             # Grosor de la letra
  FONT_SLANTS = ["roman", "italic"]                                             # Estilo de la letra

  def __init__(self, service, error_handler=None):
    """Inicializa el gestor de credenciales."""
    self.service = service                                                      # Nombre del servicio para el que se gestionan las credenciales
    self.error_handler = error_handler or self._default_error_handler           # Manejador de errores predeterminado
    metricas = self._metrics(1, 1)                                              # Obtiene la resolución del monitor en porcentaje

    # UI params
    self.border = 10                                                            # grosor del borde
    self.px = 10                                                                # Padding en x (espacio entre widgets)
    self.py = 10                                                                # Padding en y (espacio entre widgets)
    self.f_size = int(metricas[0])                                              # Tamaño de la fuente
    self.font1 = None                                                           # Fuente principal
    self.font2 = None                                                           # Fuente secundaria

  def _metrics(self, porcent_x: int, porcent_y: int):
    """metodo estatico que permite obtener un porcentaje de la resolucion del monitor
    args:
      - porcent_x (int): Porcentaje del ancho de la resolución del monitor.
      - porcent_y (int): Porcentaje de la altura de la resolución del monitor.
    Returns:
      _ tuple: porcentaje de la resolución del monitor (ancho, alto).
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

  def _setup_fonts(self):
    """metodo estatico que configura las fuentes para la interfaz grafica """
    self.font1 = tkFont.Font(family=self.FONT_FAMILIES[3], size=self.f_size, weight=self.FONT_WEIGHTS[1], slant=self.FONT_SLANTS[1]) # Fuente principal
    self.font2 = tkFont.Font(family=self.FONT_FAMILIES[3], size=self.f_size, weight=self.FONT_WEIGHTS[1], slant=self.FONT_SLANTS[0]) # Fuente secundaria

  def _build_frame(self, title: str):
    """metodo estatica que construye el frame principal de la interfaz grafica
    args:
      - title (str): Título de la ventana.
    Returns:
      - frame (tk.Frame): El marco principal de la interfaz gráfica.
    """
    self.root = tk.Tk()                                                         # creacion de la ventana raiz (interfaz grafica)
    self.root.title('Gestor de credenciales')                                   # Titulo de la ventana raiz
    self.root.resizable(False, False)                                           # habilita o inabilida el cambio de tamaño de la ventana en el eje X o Y
    self._setup_fonts()                                                         # configuracion de las fuentes
    frame = tk.Frame(self.root, bg=self.COLORS[0], bd=self.border, relief="groove") # creacion del frame principal
    frame.pack(side="top")                                                      # posicionamiento del frame en la parte superior de la ventana
    tk.Label(frame, text=title, bg=self.COLORS[0], fg=self.COLORS[8], font=self.font1).grid(row=0, column=0, columnspan=2, padx=self.px, pady=self.py) # creacion de widget tipo label (etiqueta principal)
    return frame                                                                # retorno del frame principal

  def _create_labeled_entry(self, label_text: str, variable: tk.StringVar, row: int, show: str=None, focal: bool=False):
    """metodo estatico que crea un campo de entrada con etiqueta
    args:
      - label_text (str): Texto de la etiqueta.
      - variable (tk.StringVar): Variable asociada al campo de entrada.
      - row (int): Fila en la que se coloca el widget.
      - show (str, optional): Caracter a mostrar en lugar del texto ingresado.
      - focal (bool, optional): Si se debe establecer el foco en el campo de entrada.
    """
    tk.Label(self.frame, text=label_text, bg=self.COLORS[0], fg=self.COLORS[1],font=self.font1).grid(row=row, column=0, sticky="w", padx=self.px, pady=self.py) # creacion de widget tipo label (etiqueta)
    entry = tk.Entry(self.frame, textvariable=variable, show=show, justify="left", font=self.font2, width=20) # creacion de widget tipo entry (campo de texto - textbox)
    entry.grid(row=row, column=1, sticky="w", padx=self.px, pady=self.py)       # posicionamiento del campo de texto
    if focal == True:                                                           # condicion, si focal es verdadero
      entry.focus()                                                             # establece el foco en el campo de entrada

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

  def gui_save(self):
    """Crea la interfaz gráfica para guardar las credenciales."""
    self.frame = self._build_frame(f"Guardar Credenciales de {self.service}")   # Construye el marco principal de la interfaz gráfica
    self.uid = tk.StringVar(value=getpass.getuser())                            # creacion de variable tipo StringVar, se inicializa con el nombre de usuario del sistema
    self.password = tk.StringVar()                                              # creacion de variable tipo StringVar
    self.master_key = tk.StringVar()                                            # creacion de variable tipo StringVar

    self._create_labeled_entry("USUARIO:", self.uid, row=1)                     # creacion de widgets tipo label y entry
    self._create_labeled_entry("CONTRASEÑA:", self.password, row=2, show="*", focal=True) # creacion dd widgets tipo label y entry
    self._create_labeled_entry("CLAVE MAESTRA:", self.master_key, row=3, show="*") # creacion de widgets tipo label y entry

    tk.Button(self.frame, text="ACEPTAR", command=self.save, cursor="hand2", font=self.font1, bd=self.border, relief="raised").grid(row=4, column=0, columnspan=2, padx=self.px, pady=self.py) # creacion de widget tipo button

    self._run_mainloop()                                                        # inicia el bucle principal de la ventana

  def gui_load(self):
    """Crea la interfaz gráfica para cargar las credenciales."""
    self.frame = self._build_frame(f"Leer Credenciales de {self.service}")      # Construye el marco principal de la interfaz gráfica
    self.master_key = tk.StringVar()                                            # creacion de variable tipo StringVar
    self._create_labeled_entry("CLAVE MAESTRA:", self.master_key, row=1, show="*") # creacion de widgets tipo label y entry

    tk.Button(self.frame, text="ACEPTAR", command=self.load, cursor="hand2", font=self.font1, bd=self.border, relief="raised").grid(row=2, column=0, columnspan=2, padx=self.px, pady=self.py) # creacion de widget tipo button

    self._run_mainloop()                                                        # inicia el bucle principal de la ventana

  def _derive_key(self, key: str, salt: bytes):
    """metodo estatico que deriva una clave binaria segura desde una llave usando PBKDF2-HMAC-SHA256.

    Args:
      - key (str): Clave maestra ingresada por el usuario.
      - salt (bytes): Valor aleatorio para proteger contra ataques por diccionario.

    Returns:
      - bytes: Clave derivada, codificada en base64, lista para usar con Fernet.
    """
    kdf = PBKDF2HMAC(                                                           # crea un objeto KDF (Key Derivation Function) para derivar la clave
      algorithm=hashes.SHA256(),                                                # Hash seguro
      length=32,                                                                # Longitud de clave deseada (256 bits)
      salt=salt,                                                                # Salt para hacer la derivación única
      iterations=100_000,                                                       # Repeticiones para aumentar el coste computacional y evitar ataques de fuerza bruta
      backend=default_backend()                                                 # Motor criptográfico
    )
    return base64.urlsafe_b64encode(kdf.derive(key.encode()))              # retorna la clave en formato base64 URL-safe (Fernet requiere este formato)

  def save(self):
    """Guarda las credenciales cifradas en el almacén seguro del sistema."""
    if not self.uid.get() or not self.password.get() or not self.master_key.get(): # condicion, Verifica si alguno de los campos está vacío
      messagebox.showerror("¡Error!", "Todos los campos son obligatorios.")     # despliega mensaje de error
      logging.error("Todos los campos son obligatorios.")                       # Mensaje de error
      return

    nuid = self.uid.get()                                                       # obtiene el valor del campo de texto
    npassword = self.password.get()                                             # obtiene el valor del campo de texto
    nmasterkey = self.master_key.get()                                          # obtiene el valor del campo de texto
    self.uid.set("")                                                            # Limpia el campo de texto del nombre de usuario
    self.password.set("")                                                       # Limpia el campo de texto de la contraseña
    self.master_key.set("")                                                     # Limpia el campo de texto de la clave maestra

    try:
      # Generar salt y derivar clave
      salt = os.urandom(16)                                                     # Genera un salt aleatorio de 16 bytes para proteger la clave maestra
      key = self._derive_key(nmasterkey, salt)                                  # llamado a funcion - Deriva la clave a partir de la clave maestra y el salt
      fernet = Fernet(key)                                                      # Crea un objeto Fernet con la clave derivada para cifrar y descifrar datos

      # Cifrar la contraseña
      encrypted_pwd = fernet.encrypt(npassword.encode())                        # Cifra la contraseña usando el objeto Fernet
      encoded = base64.b64encode(salt + encrypted_pwd).decode()                 # Combina el salt y la contraseña cifrada, y codifica todo en base64 para almacenamiento

      # Guardar en el almacén seguro
      keyring.set_password(self.service, "user", nuid)                          # Guarda usuario en el almacén seguro del sistema
      keyring.set_password(self.service, nuid, encoded)                         # Guarda contraseña cifrada bajo el nombre de usuario
      logging.info(f"Credenciales cifradas guardadas para '{self.service}'.")   # Mensaje de control
    except Exception as e:
      messagebox.showerror("Error", f"No se pudieron guardar las credenciales: {str(e)}") # despliega mensaje de error
      logging.error(f"Error al guardar las credenciales: {str(e)}")             # Mensaje de error
    finally:
      self.root.destroy()                                                       # destruye la ventana raiz

  def load(self):
    """Carga las credenciales cifradas del almacén seguro del sistema."""
    if not self.master_key.get():                                               # condicion, Verifica si el campo de la clave maestra está vacío
      messagebox.showerror("¡Error!", "El campo CLAVE MAESTRA no puede estar vacío.") # despliega mensaje de error
      logging.error("El campo CLAVE MAESTRA no puede estar vacío.")             # Mensaje de error
      return

    nmasterkey = self.master_key.get()                                          # obtiene el valor del campo de texto
    self.master_key.set("")                                                     # Limpia el campo de texto de la clave maestra

    try:
      # Recuperar usuario y contraseña cifrada
      nuid = keyring.get_password(self.service, "user")                         # Recupera el nombre de usuario del almacén seguro del sistema
      if nuid is None:                                                          # Verifica si el usuario existe
        raise ValueError("Usuario no encontrado.")                              # Lanza un error si no se encuentra el usuario

      encrypted = keyring.get_password(self.service, nuid)                      # Recupera la contraseña cifrada del almacén seguro del sistema
      if encrypted is None:                                                     # Verifica si la contraseña cifrada existe
        raise ValueError("Contraseña cifrada no encontrada.")                   # Lanza un error si no se encuentra la contraseña cifrada

      # Decodificar y descifrar
      raw = base64.b64decode(encrypted.encode())                                # Decodifica la contraseña cifrada de base64
      salt = raw[:16]                                                           # Extrae el salt de los primeros 16 bytes
      encrypted_pwd = raw[16:]                                                  # Extrae la contraseña cifrada
      key = self._derive_key(nmasterkey, salt)                                  # Deriva la clave usando la clave maestra y el salt
      fernet = Fernet(key)                                                      # Crea un objeto Fernet con la clave derivada
      password = fernet.decrypt(encrypted_pwd).decode()                         # Descifra la contraseña usando el objeto Fernet
      logging.info(f"Credenciales recuperadas para '{self.service}'.")          # Mensaje de control
      return nuid, password                                                     # Retorna el usuario y la contraseña descifrada
    except Exception as e:                                                      # Manejo de excepciones
      messagebox.showerror("Error", str(e))                                     # despliega mensaje de error
      logging.error(f"Error al recuperar las credenciales: {str(e)}")           # Mensaje de error
    finally:
      self.root.destroy()                                                       # destruye la ventana

  @staticmethod
  def _default_error_handler(e):
    """metodo estatico que maneja errores de forma predeterminada"""
    messagebox.showerror("Error", str(e))                                       # Muestra un mensaje de error
    logging.error(f"Error: {str(e)}")                                           # Mensaje de error
    sys.exit(1)                                                                 # salida del sistema con codigo 1 (0: sin errores, 1: con errores)