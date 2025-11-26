"""
Created on 18/05/2025
@author: frposada

Utilidades externas y soporte para integración con otras bibliotecas.
"""
#%%-------------------------------- Librerias ----------------------------------
import os
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
import pandas as pd                                                             # para el manejo y analisis de estructuras de datos
import getpass                                                                  # permite solicitar al usuario que ingrese información sensible (como contraseñas) desde la terminal sin mostrar lo que escribe en pantalla (biblioteca estandar)

#%%---------------------------- funciones y clases -----------------------------
def read_table(table_locator):
  """Lee una tabla de una página web y devuelve su contenido como una lista de listas.

  Args:
    - table_locator (WebElement): Localizador de la tabla en la página web.
  Returns:
    - list: Contenido de la tabla como una lista de listas.
  """
  from selenium.webdriver.support import expected_conditions as EC              # este modulo permite realizar las esperas explicitas, es decir el programa espera hasta que se cumpla la condicion
  from selenium.webdriver.common.by import By                                   # este modulo permite identificar objetos por (by) un atributo especifico del elemento como: name, id, etc (Se usa principalmente para los explicit wait)

  rows = []                                                                     # creacion de vector vacio para almacenar las filas de la tablas
  columns = []                                                                  # creacion de vector vacio para almacenar las columnas
  tr_contents = table_locator.find_elements(By.TAG_NAME,'tr')                   # identificacion de los tr de la tabla (filas)
  for tr in tr_contents:                                                        # ciclo para recorrer las filas de la tabla
    for td in tr.find_elements(By.TAG_NAME,'td'):                               # ciclo para recorrer las columnas de la tabla (td)
      columns.append(td.text)                                                   # se agrega al vector vacio cada uno de los textos dentro de las columnas (se arma una fila)
    rows.append(columns)                                                        # se agrega la fila al vector vacio
    columns = []                                                                # se reinicia el vector de columnas
  return(rows)                                                                  # retorno de la funcion

def send_mail(subject, body, to, cc=None, bcc=None, attachments=None):
  """Envía un correo electrónico utilizando Outlook.
  Args:
    - subject (str): Asunto del correo.
    - body (str): Cuerpo del correo en formato HTML.
    - to (list): Lista de destinatarios.
    - cc (list, optional): Lista de destinatarios en copia. Por defecto es None.
    - bcc (list, optional): Lista de destinatarios en copia oculta. Por defecto es None.
    - attachments (list, optional): Lista de archivos adjuntos.

  note:
    - es necesario tener abierto el correo, de lo contrario los correos se enviaran en cuanto se abra el correo
  """
  import win32com.client as win32                                               # permite interactuar con objetos COM y automatizar aplicaciones de Windows

  outlook = win32.Dispatch("outlook.application")                               # creacion de objeto mediante el cual se enviara las instruccion a la aplicacion de windows
  mail = outlook.CreateItem(0)                                                  # creacion de objeto "correo electronico" - En Outlook el correo electrónico, la invitación a una reunión, el calendario, la cita, etc. se consideran objetos de elemento.

  #mail.SentOnBehalfOfName = "frposada@bancolombia.com.co"                      # remitente
  mail.To = ";".join(to)                                                        # Para: Destinatario del correo electrónico. transformacion de lista en string con elementos separados por ';'
  if cc:                                                                        # condicion para verificar si existen destinatarios CC
    mail.CC = ";".join(cc)                                                      # CC o Copia de carbón: para enviar copias del correo
  if bcc:                                                                       # condicion para verificar si existen destinatarios CCO
    mail.BCC = ";".join(bcc)                                                    # CCO o Copia de carbón oculta: para enviar copias privadas del correo (ni los "Para" ni los "CC" sabran que se envio el correo a los "CCO")

  mail.Subject = subject                                                        # asunto del correo
  mail.BodyFormat = 2                                                           # Especifica el formato del texto del cuerpo a usar (2: formato HTML)
  mail.HTMLBody = body                                                          # definicion del cuerpo del correo - este debe ser escrito en formato HTML
  #mail.Body = "<H2>Mi primer mensaje</H2>"                                     # definicion del cuerpo del correo - se mostrara literalmente lo que se escriba

  if attachments:                                                               # condicion para verificar si existen archivos que adjuntar
    for attachment in attachments:                                              # ciclo para recorrer los archivos adjuntos
      mail.Attachments.Add(attachment)                                          # agrega el adjunto

  #mail.display()                                                               # permite visualizar el correo
  mail.Send()                                                                   # envio del correo
  logging.info("Correo enviado.")

def df_to_html(df):
  """Convierte un DataFrame de pandas a una tabla HTML.
  Args:
    - df (DataFrame): DataFrame que se desea convertir a código HTML.
  Returns:
    - str: Código HTML de la tabla.
  """
  table = {                                                                     # diccionario con los elementos de una tabla en html
  "stable":"<table border='1' bgcolor='black'",                                 # inicio tabla
  "etable":"</table>",                                                          # fin tabla
  "shead":"<thead>",                                                            # inicio encabezado tabla
  "ehead":"</thead>",                                                           # fin encabezado tabla
  "sbody":"<tbody>",                                                            # inicio cuerpo tabla
  "ebody":"</tbody>",                                                           # fin cuerpo tabla
  "str":"<tr>",                                                                 # inicio fila
  "etr":"</tr>",                                                                # fin fila
  "sth":"<th bgcolor='navy'>",                                                  # inicio columna resaltada
  "eth":"</th>",                                                                # fin columna resaltada
  "std":"<td bgcolor='white'>",                                                 # inicio columna normal
  "etd":"</td>",                                                                # fin columna normal
  }

  # creacion del thead -  encabezado
  columnas = df.columns.values                                                  # obtencion del nombre de las columnas del df
  y = ""                                                                        # string vacio, para anidar las columnas
  for i in range(df.shape[1]):                                                  # ciclo para recorrer columnas del df
    y = y + table["sth"] + columnas[i] + table["eth"]                           # anidacion de las columnas

  thead = table["shead"] + table["str"] + y + table["etr"] + table["ehead"]     # definicion del thead

  # creacion del tbody -  cuerpo
  x = ""                                                                        # string vacio, para anidar las filas
  for i in range(df.shape[0]):                                                  # ciclo para recorrer filas del df
    y = ""                                                                      # string vacio, para anidar las columnas
    for j in range(df.shape[1]):                                                # ciclo para recorrer columnas del df
      if str(df.iloc[i][j]) == "nan":                                           # condicion para verificar si es una celda vacia
        y = y + table["std"] + "" + table["etd"]                                # anidacion de las columnas
      else:
        y = y + table["std"] + str(df.iloc[i][j]) + table["etd"]                # anidacion de las columnas
    x = x + table["str"] + y + table["etr"]                                     # anidacion de las filas

  tbody = table["sbody"] + x + table["ebody"]                                   # definicion del tbody

  # creacion de la tabla
  tabla = table["stable"] + thead + tbody + table["etable"]                     # definicion de la tabla
  return (tabla)                                                                # retorno de la funcion

#%% #! NO USAR PARA CARGAR INFO EN TABLAS HISTORICAS, POR Q SE PIERDE LA INFO ANTERIOR (se sobreescribe)

def load_lz_nube(df, zona, tabla, dsn=None, endpoint=None, user=None, pwd=None):
  """
  Carga un DataFrame a la zona indicada de LZ nube (CDP) usando Impala Helper.
  Args:
    - df (pd.DataFrame): DataFrame a cargar.
    - zona (str): Nombre de la zona destino.
    - tabla (str): Nombre de la tabla destino.
    - dsn (str, optional): DSN configurado para nube. Por defecto es None.
    - endpoint (str, optional): URL del endpoint de CDP. Por defecto es None.
    - user (str, optional): Usuario para la conexión. Si None, se usa el usuario actual del sistema.
    - pwd (str, optional): Contraseña para la conexión. Si None, se solicita al usuario.
  note:
    - Si no se proporciona un DSN, se utilizará el DSN predeterminado 'Impala-cdp-kudu'.
    - Si no se proporciona un endpoint, se utilizará el endpoint predeterminado 'https://bancolombia-de-prd01-gateway.bco-cdp.i5u2-f1yr.cloudera.site/bancolombia-de-prd01/cdp-proxy-api/'.
  """
  from ImpalaHelper.Impala_Helper import Helper                                 # Clase para interactuar con Impala (interactuar con lz tierra y nube). #?pip install ImpalaHelper

  logging.info("Cargando archivo a LZ nube (CDP)...")                           # mensaje de control

  # parametros de conexion
  if user is None:                                                              # condicion para verificar si el usuario es None
    user = getpass.getuser()                                                    # si el usuario es None, se obtiene el usuario actual del sistema
  if pwd is None:                                                               # condicion para verificar si la contraseña es None
    pwd = getpass.getpass(prompt=f"{user}, por favor ingrese su contraseña: ")  # si la contraseña es None, se solicita al usuario que ingrese su contraseña
  if dsn is None:                                                               # condicion para verificar si el DSN es None
    dsn = 'Impala-cdp-kudu'                                                     # nombre del DSN (Data Source Name) que se configura en el ODBC (LZ nube - CDP)
  if endpoint is None:                                                          # condicion para verificar si el endpoint es None
    endpoint = 'https://bancolombia-de-prd01-gateway.bco-cdp.i5u2-f1yr.cloudera.site/bancolombia-de-prd01/cdp-proxy-api/' # URL Endpoint CDP sobre el cual correrá la rutina

  serverOpts = {'user': user, 'password': pwd, 'cloud_server': endpoint}        # Diccionario con las credenciales de conexión
  hp = Helper({'connStr': f'DSN={dsn}'}, cloud=True)                            # Instanciar helper especificando el string de conexión odbc, zona por defecto y si se va a trabajar en nube o tierra
  try:
    hp.fromPandasDF(df, f'{zona}.{tabla}', serverOpts)                          # Subir tabla desde DataFrame
    logging.info("Archivo cargado exitosamente a LZ nube (CDP)...")             # mensaje de control
  except Exception as e:                                                        # captura de excepciones
    logging.error(f"Error al cargar el DataFrame a LZ nube: {e}")               # mensaje de error
  finally:
    hp.close()

def load_lz_tierra(df, zona, tabla, dsn=None, user=None, pwd=None):
  """
  Carga un DataFrame a la zona indicada de LZ tierra usando Impala Helper.
  Args:
    - df (pd.DataFrame): DataFrame a cargar.
    - zona (str): Nombre de la zona destino.
    - tabla (str): Nombre de la tabla destino.
    - dsn (str, optional): DSN configurado para tierra. Por defecto es None.
    - user (str, optional): Usuario para la conexión. Si None, se usa el usuario actual del sistema.
    - pwd (str, optional): Contraseña para la conexión. Si None, se solicita al usuario.
  note:
    - Si no se proporciona un DSN, se utilizará el DSN predeterminado 'impala-virtual-prd'.
    """
  from ImpalaHelper.Impala_Helper import Helper                                 # Clase para interactuar con Impala (interactuar con lz tierra y nube). #?pip install ImpalaHelper

  logging.info("Cargando archivo a LZ tierra...")                               # mensaje de control

  # parametros de conexion
  if user is None:                                                              # condicion para verificar si el usuario es None
    user = getpass.getuser()                                                    # si el usuario es None, se obtiene el usuario actual del sistema
  if pwd is None:                                                               # condicion para verificar si la contraseña es None
    pwd = getpass.getpass(prompt=f"{user}, por favor ingrese su contraseña: ")  # si la contraseña es None, se solicita al usuario que ingrese su contraseña
  if dsn is None:                                                               # condicion para verificar si el DSN es None
    dsn = 'impala-virtual-prd'                                                  # nombre del DSN (Data Source Name) que se configura en el ODBC (LZ nube - CDP)
  host = 'sbmdeblze004.bancolombia.corp'                                        # nombre del host (servidor) al que se conecta (opcional)

  serverOpts_tierra = {'user': user, 'password': pwd, 'host': host}             # Diccionario con las credenciales de conexión
  hp = Helper({'connStr': f'DSN={dsn}'}, cloud=False)                           # Instanciar helper especificando el string de conexión odbc, zona por defecto y si se va a trabajar en nube o tierra
  try:
    hp.fromPandasDF(df, f'{zona}.{tabla}', serverOpts_tierra)                   # Subir tabla desde DataFrame
    logging.info("Archivo cargado exitosamente a LZ tierra...")                 # mensaje de control
  except Exception as e:                                                        # captura de excepciones
    logging.error(f"Error al cargar el DataFrame a LZ tierra: {e}")             # mensaje de error
  finally:                                                                      # finally se ejecuta siempre, sin importar si hay un error o no
    hp.close()                                                                  # Cerrar conexión

def load_lz_tierra_sparky(df, zona, tabla, dsn=None):
  """
  Carga un DataFrame a la zona de procesos de LZ tierra usando Sparky.
  Args:
    df (pd.DataFrame): DataFrame a cargar.
    zona (str): Nombre de la zona destino.
    tabla (str): Nombre de la tabla destino.
    dsn (str, optional): DSN configurado para tierra. Por defecto es None.
  note:
    - Si no se proporciona un DSN, se utilizará el DSN predeterminado 'impala-virtual-prd'.
  """
  from sparky_bc import Sparky                                                  # Clase para interactuar con Spark y en los servidores del Banco (Subir info a la LZ-tierra)

  logging.info("Cargando archivo a LZ tierra...")                               # mensaje de control

  # parametros de conexion
  user = getpass.getuser()                                                      # Usuario
  host = 'sbmdeblze004.bancolombia.corp'                                        # nombre del host (servidor) al que se conecta (opcional)
  if dsn is None:                                                               # condicion para verificar si el DSN es None
    dsn = 'impala-virtual-prd'                                                  # nombre del DSN (Data Source Name) que se configura en el ODBC (LZ nube - CDP)

  sp = Sparky(username=user, dsn=dsn, hostname=host)                            # instancia (objeto) de la clase Sparky
  try:
    sp.subir_df(df, f'{zona}.{tabla}', modo='overwrite')                        # Subir tabla desde DataFrame, modo overwrite (sobreescribe la tabla)
    logging.info("Archivo cargado exitosamente a LZ tierra...")                 # mensaje de control
  except Exception as e:                                                        # captura de excepciones
    logging.error(f"Error al cargar el DataFrame a LZ tierra: {e}")             # mensaje de error
  finally:                                                                      # finally se ejecuta siempre, sin importar si hay un error o no
    sp.close()                                                                  # Cerrar conexión

def odbc(dsn, sql_query=None, path_sql=None, user=None, pwd=None):
  """
  Ejecuta una consulta ODBC usando un DSN y retorna el resultado como DataFrame.
  Args:
    - dsn (str): Nombre del DSN configurado en ODBC.
    - sql_query (str, optional): Consulta SQL a ejecutar directamente.
    - path_sql (str, optional): Ruta a archivo .sql con la consulta.
    - user (str, optional): Usuario ODBC. Si None, usa el usuario de la sesión.
    - pwd (str, optional): Contraseña ODBC. Si None, la solicita por consola.
  Returns:
    - dict: Diccionario con los resultados de las consultas ejecutadas. Las llaves son 'direct' y/o 'archivo', según lo ejecutado.
  """
  import pyodbc                                                                 # para la conexion ODBC y ejecucion de consultas SQL

  # parametros de conexion
  if user is None:                                                              # condicion para verificar si el usuario es None
    user = getpass.getuser()                                                    # si el usuario es None, se obtiene el usuario actual del sistema
  if pwd is None:                                                               # condicion para verificar si la contraseña es None
    pwd = getpass.getpass(prompt=f"{user}, por favor ingrese su contraseña: ")  # si la contraseña es None, se solicita al usuario que ingrese su contraseña

  connection_string = f"DSN={dsn};UID={user};PWD={pwd}"                         # Cadena de conexión ODBC con DSN, usuario y contraseña
  resultados = {}                                                               # Diccionario para almacenar los resultados de las consultas ejecutadas

  try:
    with pyodbc.connect(connection_string, autocommit=True) as conn:            # Establecer conexión ODBC con autocommit para evitar problemas de transacciones
      logging.info(f"Conexión ODBC exitosa a DSN: {dsn}")                       # Mensaje de control
      cursor = conn.cursor()                                                    # Crear objeto cursor para ejecutar consultas SQL
      if sql_query:                                                             # Verificar si se proporcionó una consulta SQL directa
        cursor.execute(sql_query)                                               # Ejecutar consulta SQL
        resultados['direct'] = pd.DataFrame([tuple(row) for row in cursor.fetchall()], columns=[desc[0] for desc in cursor.description]) # Convertir resultados a DataFrame y almacenarlo en el diccionario
      if path_sql:                                                              # Verificar si se proporcionó una ruta a un archivo SQL
        with open(path_sql, "r") as file:                                       # Abrir el archivo SQL en modo lectura
          sql_query2 = file.read()                                              # Leer el contenido del archivo SQL
        cursor.execute(sql_query2)                                              # Ejecutar la consulta SQL leída del archivo
        resultados['archivo'] = pd.DataFrame([tuple(row) for row in cursor.fetchall()], columns=[desc[0] for desc in cursor.description]) # Convertir resultados a DataFrame y almacenarlo en el diccionario)
  except pyodbc.Error as e:                                                     # Captura de excepciones ODBC
    logging.error(f"Error de conexión ODBC: {e}")                               # Mensaje de error si ocurre un problema al conectar o ejecutar la consulta
  except FileNotFoundError:                                                     # Captura de excepción si no se encuentra el archivo SQL
    logging.error("No se encontró el archivo SQL")                              # Mensaje de error si no se encuentra el archivo SQL
  return resultados                                                             # Retornar el diccionario con los resultados de las consultas ejecutadas

  # Parámetros de conexión nacional sin DSN
  # driver = '{iSeries Access ODBC Driver}'                                       # Nombre del driver ODBC (controlador q permite trabajar con bases de datos a travez del estandar ODBC)
  # system = 'NACIONALET01'                                                       # nombre del sistema (se usa en lugar de especificar el servidor) #?(Ambos sirven)
  # system = '10.9.2.201'                                                         # nombre del sistema (se usa en lugar de especificar el servidor) #?(Ambos sirven)
  # port = '992'                                                                  # numero del puerto usado para la conexion (opcional - no se recomienda ya q los usuarios pueden tener establecido otro puerto de conexion)
  # database = 'VISIONR'                                                          # base de datos (opcional - solo usar si todas las tablas q vas a consultar pertenecen a la misma BD) (No logre hacer q funcionara)

  # connection_string = f"DRIVER={driver};SYSTEM={system};UID={user};PWD={pwd};AUTHENTICATION=0" # cadena de conexion, contiene la informacion necesaria para establecer la conexion con la fuente de datos. "AUTHENTICATION" - especifica el metodo de autentificacion, 0: servidor, 1: windows. Usando 1 se realiza la conexion a la BD con las credenciales de inicio de sesion de windows
