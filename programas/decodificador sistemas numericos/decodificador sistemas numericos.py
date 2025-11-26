# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:07:33 2022
@author: frposada
"""

import pandas as pd                                                             # para el manejo y analisis de estructuras de datos
import time                                                                     # para el manejo del tiempo

#%%------------------------ Variables globales ---------------------------------

start_time = time.time()                                                        # Guarda el tiempo inicial - para reconocer cuanto tarde el programa en ejecutarse
base = 2

#%%------------------------ Definicion de funciones ----------------------------

def decoder():                                                                  # definicion de funcion (Decodifica los numeros dependiendo de su base a base 10)
  df = pd.DataFrame()                                                           # creacion de dataframe vacio
  for j in range(codigo.shape[1]):                                              # ciclo para recorrer columnas del df
    lista = []                                                                  # creacion lista vacia, para almacenar los datos de las columnas
    for i in range(codigo.shape[0]):                                            # ciclo para recorrer filas del df
      numero = str(codigo.iloc[i][j])                                           # lectura del numero
      numero_decimal = int(numero,base)                                         # Tranformacion a base 10
      lista.append(numero_decimal)                                              # se agrega el dato a la lista
    df[str(j)] = lista                                                          # se agrega la lista a una nueva columna del df
  return(df)

def decoder_ascii (base10):                                                     # definicion de funcion (Decodifica los numeros en base 10 a su representativo en codigo ascii)
  df = pd.DataFrame()                                                           # creacion de dataframe vacio
  for j in range(base10.shape[1]):                                              # ciclo para recorrer columnas del df
    lista = []                                                                  # creacion lista vacia, para almacenar los datos de las columnas
    for i in range(base10.shape[0]):                                            # ciclo para recorrer filas del df
      x = chr(base10.iloc[i][j])                                                # decodificacion del numero en base 10 a su representacion en ascii
      lista.append(x)                                                           # se agrega el dato a la lista
    df[str(j)] = lista                                                          # se agrega la lista a una nueva columna del df
  return (df)                                                                   # retorno de funcion

#%%---------------------------- Main Function ---------------------------------

codigo = pd.read_excel("Codigo.xlsx", header = None)                            # Lectura del archivo de excel especificado

if base == 10:                                                                  # condicion en caso de que el cifrado sea en base 10
  base10 = codigo
else:
  base10 = decoder()                                                            # llamado a funcion

mensaje = decoder_ascii(base10)                                                 # llamado a funcion

nombre = "Decodificacion.xlsx"
writer = pd.ExcelWriter(nombre)

codigo.to_excel(writer, sheet_name = "Base" + str(base), index = False, header=None)
base10.to_excel(writer, sheet_name = "Base 10", index = False, header=None)
mensaje.to_excel(writer, sheet_name = "Mensaje", index = False, header=None)
writer.save()

fin = time.time()

print(fin)