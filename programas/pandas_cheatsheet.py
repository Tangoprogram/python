"""
Created on 13/05/2025
pandas_cheatsheet
@author: frposada
"""
#%%-------------------------------- Librerias ----------------------------------
import pandas as pd
import numpy as np

#%% ------------------------- CREACIÓN DE DATAFRAMES ---------------------------
# DataFrame vacío
df = pd.DataFrame()                                                             # También útil para reiniciar un DataFrame

# Creación por filas
df = pd.DataFrame(
  [
    [1, 'Juan', 25.0, '2025-01-01', True, 1000.50],
    [2, 'María', 30.0, '2025-02-02', False, 2000.75],
    [3, 'Pedro', 35.0, '2025-03-03', True, -500.25],
    [4, 'Luis', np.nan, '2025-04-04', True, 0.00],
    [5, 'Ana', 40.0, '2025-05-05', False, 1500.00]
  ],
  columns=['ID', 'Nombre', 'Edad', 'Fecha', 'Activo', 'Saldo']
)

# Creación por columnas (dict)
diccionario = {
  'ID': [1, 2, 3, 4, 5],
  'Nombre': ['Juan', 'María', 'Pedro', 'Luis', 'Ana'],
  'Edad': [25, 30, 35, np.nan, 40],  # Incluye un valor nulo
  'Fecha': ['2025-01-01', '2025-02-02', '2025-03-03', '2025-04-04', '2025-05-05'],  # Fechas como strings
  'Activo': [True, False, True, True, False],  # Valores booleanos
  'Saldo': [1000.50, 2000.75, -500.25, 0, 1500.00]  # Valores numéricos positivos y negativos
}
df2 = pd.DataFrame(diccionario)

#%% ----------------------- MODIFICACIÓN DE DATAFRAMES -------------------------
# campos - columnas
df['apellido'] = ['Savato', 'Gonzalez', 'Lopez', 'Martinez', 'Hernandez']       # Agregar columna
df = df.drop(columns=['apellido'])                                              # Eliminar columna por nombre

# registros - filas
df = df.drop([0, 1], axis=0).reset_index(drop=True)                             # Eliminar registros por índice y reiniciar índice

# Agregar registro con loc (util para un solo registro - necesario especificar el valor de cada campo)
df.loc[len(df)] = [6, 'Frank', 30, '2025-06-06', True, 3000.00]                 # Agregar registro al final (de lo contrario remplazaria el dato de la posición que se indique)

# Agregar registros con concat (util para varios registros - no es necesario especificar el valor de cada campo)
nuevo_df = pd.DataFrame({'ID': [0, 1], 'Nombre': ['Michael', 'Elizabet'], 'Saldo': [300, 1000]}) # Crear un nuevo registro como un DataFrame
df = pd.concat([df, nuevo_df], ignore_index=True)                               # Concatenar DataFrames

#%% ---------------------- LECTURA Y ESCRITURA DE VALORES ----------------------
df.loc[0, 'Edad'] = 60                                                          # Asignar valor a celda
x = df.loc[0]['Edad']                                                           # Leer valor de celda

#%% ---------------------------- TIPOS DE DATOS --------------------------------
tipos = df.dtypes                                                               # Ver tipo de datos de columnas
df = df.astype({'Fecha': 'datetime64[ns]', 'Activo': 'bool'})                   # Cambiar tipo de datos de columnas
tipos2 = df.dtypes                                                              # Ver tipo de datos de columnas

#%% ------------------------------- FILTRADO -----------------------------------
mask = df['Edad'] > 30                                                          # Crear una máscara booleana
df_filtrado1 = df[mask]                                                         # Filtrar DataFrame

df_filtrado2 = df[df['Edad'] > 30]                                              # Filtrar DataFrame directamente

df_filtrado3 = df[(df['Edad'] > 30) & (df['Activo'] == True)]                   # Filtrar con múltiples condiciones


#%% ----------------------------- VALORES NULOS --------------------------------
es_nulo = df['Edad'].isnull()                                                   # Booleano por fila
hay_nulos = df['Edad'].isnull().any()                                           # Algún NaN en columna
df_tiene_nulos = df.isnull().any().any()                                        # Algún NaN en el DataFrame
total_nulos_col = df['Edad'].isnull().sum()                                     # Conteo de NaNs en una columna
total_nulos_df = df.isnull().sum().sum()                                        # Total de NaNs en todo el DataFrame

#%% ------------------------ CONVERSIÓN DE DATAFRAMES --------------------------
lista1 = df.to_numpy().tolist()                                                 # Convertir DataFrame a lista de listas
lista2 = df.values.tolist()                                                     # Convertir DataFrame a lista de listas

#%% ------------------------- GUARDADO Y EXPORTACIÓN ---------------------------
df.to_csv('archivo.txt', sep='\t', index=False)                                 # Guardar DataFrame como archivo de texto
df.to_csv('archivo.csv', index=False)                                           # Guardar DataFrame como archivo CSV
df.to_excel('archivo.xlsx', index=False)                                        # Guardar DataFrame como archivo Excel (requiere openpyxl o xlrd)
df.to_json('archivo.json')                                                      # Guardar DataFrame como archivo JSON

#%% -------------------------- LECTURA DE ARCHIVOS -----------------------------
df_txt = pd.read_csv('archivo.txt', sep='\t')                                   # Leer archivo de texto con separador personalizado
df_csv = pd.read_csv('archivo.csv')                                             # Leer archivo CSV
df_excel = pd.read_excel('archivo.xlsx')                                        # Leer archivo Excel (requiere openpyxl o xlrd)
df_json = pd.read_json('archivo.json')                                          # Leer archivo JSON