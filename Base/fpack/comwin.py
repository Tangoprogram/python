"""
Created on Thu Nov 17 09:10:34 2022
este modulo implementa funciones utilizando la libreria win32
con la cual podemos interactuar con objetos COM y aplicaciones de windows
@author: frposada
"""
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
import win32com.client as win32                                                 # permite interactuar con objetos COM y automatizar aplicaciones de Windows
import pandas as pd                                                             # para el manejo y analisis de estructuras de datos

#%%------------------------ Variables globales ---------------------------------
colors = ["White", "Silver", "Gray", "Black", "Red", "Maroon", "Yellow", "Olive", "Lime", "Green", "Aqua", "Teal", "Blue", "Navy", "Fuchsia", "Purple"] # lista de los colores por defecto de html
#%%-------------------------- funciones y clases -------------------------------
def send_mail(asunto, cuerpo, para, cc = False, cco = False, adjunto = False):  # Definicion de funcion (permite enviar correos electronicos con outlook)
  outlook = win32.Dispatch("outlook.application")                               # creacion de objeto mediante el cual se enviara las instruccion a la aplicacion de windows
  mail = outlook.CreateItem(0)                                                  # creacion de objeto "correo electronico" - En Outlook el correo electrónico, la invitación a una reunión, el calendario, la cita, etc. se consideran objetos de elemento.

  #mail.SentOnBehalfOfName = "frposada@bancolombia.com.co"                      # remitente
  para =  ";".join(para)                                                        # convertimos la lista en un string con cada uno de los elementos que la componen separados por ';'
  mail.To = para                                                                # Para: Destinatario del correo electrónico

  if cc != False:                                                               # condicion para verificar si existen destinatarios CC
    cc =  ";".join(cc)                                                          # convertimos la lista en un string con cada uno de los elementos que la componen separados por ';'
    mail.CC = cc                                                                # CC o Copia de carbón: para enviar copias del correo

  if cco != False:                                                              # condicion para verificar si existen destinatarios CC
    cco =  ";".join(cco)                                                        # convertimos la lista en un string con cada uno de los elementos que la componen separados por ';'
    mail.BCC = cco                                                              # CCO o Copia de carbón oculta: para enviar copias privadas del correo (ni los "Para" ni los "CC" sabran que se envio el correo a los "CCO")

  mail.Subject = asunto                                                         # asunto del correo
  mail.BodyFormat = 2                                                           # Especifica el formato del texto del cuerpo a usar (2: formato HTML)
  mail.HTMLBody  = cuerpo                                                       # definicion del cuerpo del correo - este debe ser escrito en formato HTML
  #mail.Body = "<H2>Mi primer mensaje</H2>"                                     # definicion del cuerpo del correo - se mostrara literalmente lo que se escriba

  if adjunto != False:                                                          # condicion para verificar si existen archivos que adjuntar
    for i in adjunto:
      mail.Attachments.Add(i)                                                   # agrega el adjunto

  mail.display()                                                                # permite visualizar el correo
  #mail.Send()                                                                  # envio del correo
  logging.info("Correo enviado...")                                             # mensaje de control
  """
  Importante - es necesario tener abierto el correo, de lo contrario los correos se enviaran en cuanto se abra el correo
  asunto: string donde se especifica el asunto del correo
  cuerpo: string donde se define el cuerpo del correo, escrito en formato html
  para: listado con los Destinatarios del correo
  cc: listado con los Destinatarios de las copias del correo
  cco:listado con los Destinatarios de las copias privadas del correo
  adjunto: listado de las rutas donde se encuentran los archivos adjuntos, especifique el nombre del archivo y su extension al final de la ruta
  """

def df_to_html(df):                     # Definicion de funcion (convierte un df en una tabla en lenguaje HTML)
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
  '''
  df: dataframe que se desea convertir a codigo html
  '''