# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:16:01 2022
Funciones para el manejo de bases de datos con pandas
@author: frposada
"""
import os                                                                       # proporciona funciones para interactuar con el sistema operativo (biblioteca estandar)
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
import pandas as pd                                                             # para el manejo y analisis de estructuras de datos

#%%--------------------- Definicion de funciones ------------------------------
""" parametro opcional - tiene un valor por default por lo que no es necesario que el usuario pase este parametro"""

def save_df(path_dir,name,df, extension): # Definicion de funcion (Guarda el df seleccionado con la extension que se especifique)
  nombre = name + "." + extension                                               # se define el nombre del informe a guardar
  if extension == "xlsx":
    df.to_excel(path_dir + "/" + nombre, index = False)                         # se transforma el df a un archivo excel
  elif extension == "txt":
    df.to_csv(path_dir + "/" + nombre, index=False, sep='¡')                    # se transforma el df a un archivo txt
  """
  Path_dir: ruta donde se desea guardar el archivo
  name: nombre con el que se quiere guaradar el archivo
  df: el dataframe que se desea guardar
  extension: tipo de archivo (EJ: xlsx, txt)
  """

def read_some_files(path_dir, extension, separador = ",", in_supplied = [], encabezado = "infer", consolidation = False): # Definicion de funcion (Permite leer y consolidar diferentes archivos xlsx (excel) o csv (txt) que se encuentren en una carpeta)
  if in_supplied == []:                                                         # condicion para verificar si se leeran todos los archivos de la carpeta o solo los que se especifiquen
    in_supplied = os.listdir(path_dir)                                          # Lista de los archivos dentro de la carpeta especificada

  x = []                                                                        # creacion de lista vacia
  if extension == "xlsx":
    for i in range(len(in_supplied)):                                           # ciclo para recorrer lista
      x.append(pd.read_excel(path_dir + "/" + in_supplied[i], header = encabezado)) # Leer el archivo de excel especificado y agregarlo a la lista
      logging.info("file " + in_supplied[i] + " read")                          # mensaje de control
  elif extension == "txt":
    for i in range(len(in_supplied)):                                           # ciclo para recorrer lista
      x.append(pd.read_csv(path_dir + "/" + in_supplied[i], sep = separador, header = encabezado, engine='python', encoding_errors='ignore')) # Leer el archivo de excel especificado y agregarlo a la lista
      logging.info("file " + in_supplied[i] + " read")                          # mensaje de control
  if consolidation == True:                                                     # Condicion para verificar si se desean consolidar los archivos
    consolidado = pd.concat(x,ignore_index = True)                              # consolidacion - concatenar los archivos
    return consolidado                                                          # retorno de la funcion
  else:
    return x                                                                    # retorno de la funcion

  """
  Path_dir: ruta de la carpeta que contiene los archivos
  extension: tipo de archivos a leer (EJ: xlsx, txt(csv)
  separador: indica el separador a usar en caso de leer un archivo txt, por defecto la funcion "pd.read_csv" tiene como separador la "," por tal motivo tambien se usa esta como el valor por defecto del parametro opcional de la funcion "read_some_files"
  in_supplied: parametro opcional - lista de los archivos a leer, en caso de que no se suministre se leeran todos los archivos de la carpeta
  encabezado: parametro opcional - usar el valor por default ("infer") hace que la primera fila del archivo leido sea el nombre de los campos, en caso de que esto no se quiera escribir None
  Consolidation: parametro opcional - variable booleana, si es True consolidara los archivos

  Notas:
  * encoding_errors ='ignore', este parametro evita que se presenten errores cuando se tienen caracteres ASCII no reconocidos en el archivo a leer - no usarlo en spyder

  * engine ='python', este parametro evita que se presenten ParserWarning, producidos por que pandas utiliza un analizador rápido y eficiente implementado C (especificado como engine='c'). Actualmente, las opciones no compatibles con C incluyen:
  1) sep que no sea un solo carácter (EJ: separadores de expresiones regulares)
  2) saltarín
  3) sep = Ninguno con delim_whitespace=Falso
  si se presenta alguna de las opciones anteriores producirá un ParserWarning a menos que el motor de python se seleccione explícitamente mediante engine='python'

  Errores comunes:
  * "pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 18, saw 4"   -   este error se produce debido a que el separador identifica filas con mas columnas que las esperadas, es decir, el separador usado se encuentra mas veces de lo esperado en x fila, de hecho se te especifica la fila en que se presenta el problema, soluciones:
  1) abrir el archivo manualmente y arreglar la fila que presenta el problema
  2) usar un separador que no se encuentre en el archivo

  * pandas.errors.ParserError: '¡' expected after '"'  -   este error se produce cuando se tienen comillas sin escape (comillas de mas "). Ej:"1405246510","book","hardcover", "" "frank", "posada". solucion:
  1) elimine las comillas del documento
  2) use este parametro  -----  quoting=3 ------------  en el pd.read_csv()
  """

def inputs_identifying(path_dir_rec, path_dir): # Definicion de funcion (Identifica cuales de los archivos suministrados son reconocidos por el sistema)
  insumos_rec = pd.read_excel(path_dir_rec + "/Insumos reconocidos.xlsx")       # lectura del df con los insumos que reconoce el programa
  in_supplied = os.listdir(path_dir)                                            # Lista de los archivos dentro de la carpeta especificada
  x = []                                                                        # creacion de lista vacia
  for i in range(insumos_rec.shape[0]):                                         # ciclo para recorrer el df
    x.append(insumos_rec.iloc[i]["Insumo"] in in_supplied)                      # identificacion de los insumos reconocidos que se han suministrado
  insumos_rec = insumos_rec.assign(Encontrado = x)                              # se crea una nueva columna en el df donde se especifica si se suministro o no los insumos reconocidos
  #insumos_rec = insumos_rec[insumos_rec["Encontrado"] == True]                 # filtrado por los insumos suministrados
  return(insumos_rec)                                                           # retorno funcion
  """
  Para hacer uso de esta funcion es necesario que exista el archivo: Insumos reconocidos.xlsx, con un campo llamado: Insumo, en donde se especifique el nombre (con extension) de los archivos reconocidos por el sistema
  Path_dir_rec: ruta donde se encuentra el archivo "Insumos reconocidos"
  Path_dir: ruta de la carpeta que contiene los archivos
  """

def df_to_list (df):                    # Definicion de funcion (transforma un dataframe en una lista - El resultado es una lista que contiene 1 elemento por cada registro del df)
  df = pd.DataFrame(df)                                                         # nos aseguramos de que lo que se le suministre a la funcion sea un df
  lista = []                                                                    # creacion lista vacia
  for i in range(df.shape[0]):                                                  # ciclo para recorrer el df
    lista.append(df.iloc[i][0])                                                 # agregacion a la lista los "campos" por las que se desea filtrar
  return lista

def searchv(df,camposearch,search,campoload = "opcional"): # Definicion de funcion (identifica valores en un dataframe a partir de una llave)
  if campoload == "opcional":                                                   # condicion para verificar si no se paso el "parametro opcional" - si este campo no se suministra por el usuario se traeran todos los campos (toda la fila)
    x = df[df[camposearch] == search]                                           # se busca el "search" en el "camposearch" y se trae toda la fila (BUSCARV)
  else:
    x = df[df[camposearch] == search][campoload]                                # se busca el "search" en el "camposearch" y se trae lo que encuentre en el "campoload" (BUSCARV)
    x = pd.DataFrame(x)                                                         # conversion del arreglo a df - para retornar el mismo tipo de dato en ambos casos. Ademas permite organizar las dimensiones

  if x.empty:                                                                   # condicion para verificar si la serie esta vacia (esto sucede si el radicado analizado no tiene el Sig_estados "usuario entrada")
    logging.info("No se encontro " + str(search) + " en el campo " + camposearch) # mensaje de control
  else:
    x = x.reset_index(drop = True)                                              # reinicio de indice
  return x                                                                      # retorno de la funcion
  """
  * BuscarV
  df: dataframe en el que se va a buscar
  camposearch: en que campo buscar
  search: lo que se va a buscar
  campoload:  parametro opcional - que campo quiero traer?
  1) campoload -> valor: default -> traera todos los campos (trae toda la fila)
  2) campoload -> valor: string -> traera el campo especificado
  3) campoload -> valor: lista de strings -> traera todos los campos especificados (Use la funcion "df_to_list" para implementar facilmente esta funcion)
  """

#%% funciones a recordar

#df2 = df.values.tolist()                                               # transformacion de df a lista - El resultado es una lista que contiene 1 elemento por cada registro del df


#?   df.loc[0,'DATE'] = 3   # para asignar un valor
#?   x = df.loc[0]['DATE']  # para leer un valor

#* año = insumo["FECHA "].str.slice(start = 0, stop = 4)                        # particionar los string de la columna especificada
#* mes = insumo["FECHA "].str.slice(start = 4, stop = 6)                        # particionar los string de la columna especificada
#* dia = insumo["FECHA "].str.slice(start = 6, stop = 8)                        # particionar los string de la columna especificada
#* insumo['FECHA '] = mes + dia + año                                           # reorganizacion de las fechas en el formato adecuado

#todo df.dtypes                                                                 # permite saber el formato de los datos que componen un df
#todo df = df.astype({'columna1':'float64'})                                    # transformacion del tipo de datos de los campos especificados

#! mask = df["Edad de mora"] < 0
#! df.loc[mask, "Edad de mora"] = 0
#! df.loc[df["Edad de mora"] < 0, "Edad de mora"] = 0                           # para cambiar el valor de los datos que cumplan la condicion

#? lista = df.to_numpy().tolist()                                               # transformacion de df a lista - El resultado es una matriz, una lista que contiene 1 lista por cada registro del df
#table = pd.DataFrame() #limpiar df o crearlo desde cero
#table = table.drop([0])# eliminar registros

# x = df[i].isnull()                                                            # identifica que celdas tienen NaN - [i] para especificar una columna
# y = df[i].isnull().any()                                                      # identifica que columnas tienen alguna celda en NaN - [i] para especificar una columna
# z = df.isnull().any().any()                                                   # identifica si existe alguna celda con NaN en el df
# u = df[i].isnull().sum()                                                      # identifica la cantidad de celdas en NaN en cada columna - [i] para especificar una columna
# v = df.isnull().sum().sum()                                                   # identifica la cantidad de celdas en NaN en el df

#* formas para crear un df desde cero
# creacion por filas
# df = pd.DataFrame(
#   [['Fiduciaria - comision',1694109005,0,0],
#   ['Fiduciaria - intereses',1694959005,0,0],
#   ['Fiduciaria - otras',1694959005,0,0],
#   ['Valores',000,0,0],
#   ['Banca inversion',0,0,0],
#   ['CFNS',0,0,0]],
#   columns=['Filial', 'Cuenta provision', 'Cuenta gastos', 'Cuenta ingresos']
# )
# #---------------------------------------
# creacion por columnas
# diccionario = {
#   'Filial':['Fiduciaria - comision','Fiduciaria - intereses','Fiduciaria - otras','Valores','Banca inversion','CFNS'],
#   'Cuenta provision':[1694109005,1694959005,1694959005,0,0,0],
#   'Cuenta gastos':[0,0,0,0,0,0],
#   'Cuenta ingresos':[0,0,0,0,0,0]
# }

# df2 = pd.DataFrame(diccionario)

#* Como agregar nuevos registros a un dataframe
# # Crear un DataFrame de ejemplo
# df = pd.DataFrame({
#     'nombre': ['Juan', 'María', 'Pedro'],
#     'edad': [25, 30, 35]
# })

# # Agregar un nuevo registro utilizando la función loc - es necesario especificar el valor de cada uno de los campos
# df.loc[len(df)] = ['Luis', 40]                                                  # agregar nuevo registro

# # Agregar un nuevo registro utilizando la función concat - no es necesario especificar el valor de cada uno de los campos
# df2 = pd.DataFrame({'edad':[27], 'apellido':'Posada'})                           # Crear un nuevo registro como un DataFrame
# df = pd.concat([df, df2], ignore_index=True)                                    # Concatenar ambos DataFrames
