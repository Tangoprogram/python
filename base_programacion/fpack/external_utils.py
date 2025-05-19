"""
Created on 18/05/2025
@author: frposada

Utilidades externas y soporte para integración con otras bibliotecas.
"""
#%%-------------------------------- Librerias ----------------------------------
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)

import pandas as pd                                                             # para el manejo y analisis de estructuras de datos
from selenium.webdriver.support import expected_conditions as EC                # este modulo permite realizar las esperas explicitas, es decir el programa espera hasta que se cumpla la condicion
from selenium.webdriver.common.by import By                                     # este modulo permite identificar objetos por (by) un atributo especifico del elemento como: name, id, etc (Se usa principalmente para los explicit wait)
import win32com.client as win32                                                 # permite interactuar con objetos COM y automatizar aplicaciones de Windows

#%%---------------------------- funciones y clases -----------------------------
def read_table(table_locator):
  """Lee una tabla de una página web y devuelve su contenido como una lista de listas.

  Args:
    - table_locator (WebElement): Localizador de la tabla en la página web.
  Returns:
    - list: Contenido de la tabla como una lista de listas.
  """
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

  Importante - es necesario tener abierto el correo, de lo contrario los correos se enviaran en cuanto se abra el correo
  """

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