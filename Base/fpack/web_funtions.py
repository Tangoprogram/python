"""
Created on Tue Sep 20 11:11:36 2022
funciones utiles para la interaccion con paginas web usando la libreria selenium
@author: frposada
"""
import logging                                                                  # Permite generar un sistema de registro de eventos (biblioteca estandar)
from selenium.webdriver.support import expected_conditions as EC                # este modulo permite realizar las esperas explicitas, es decir el programa espera hasta que se cumpla la condicion
from selenium.webdriver.common.by import By                                     # este modulo permite identificar objetos por (by) un atributo especifico del elemento como: name, id, etc (Se usa principalmente para los explicit wait)

"""
Donde se ejecuta el .py estará la carpeta del Driver. Sin embargo, se copiará el archivo a una ruta relativa del usuario, se ejecuta y se elimina después
La copia se genera porque la ruta compartida no tiene puertos habilitados para acceder a la red con controladores, el computador sí.
"""
#%%--------------------- Definicion de funciones ------------------------------

def read_table(table_locator):          # Definicion de funcion (lee una tabla de una pagina web y retorna una lista (matriz) con sus componentes)
  rows = []                                                                     # creacion de vector vacio para almacenar las filas de la tablas
  columns = []                                                                  # creacion de vector vacio para almacenar las columnas
  tr_contents = table_locator.find_elements(By.TAG_NAME,'tr')                   # identificacion de los tr de la tabla (filas)
  for tr in tr_contents:                                                        # ciclo para recorrer las filas de la tabla
    for td in tr.find_elements(By.TAG_NAME,'td'):                               # ciclo para recorrer las columnas de la tabla (td)
      columns.append(td.text)                                                   # se agrega al vector vacio cada uno de los textos dentro de las columnas (se arma una fila)
    rows.append(columns)                                                        # se agrega la fila al vector vacio
    columns = []                                                                # se reinicia el vector de columnas
  return(rows)                                                                  # retorno de la funcion
  '''
  table_locator: es el localizador de la tabla en la pagina web que se este trabajando
  '''