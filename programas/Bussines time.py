"""
Created on 12/07/2025
Operaciones con fechas y horas
@author: frposada

Calculadora de Tiempo Laboral (Business Time Calculator)
"""

#%%-------------------------------- Librerias ----------------------------------
print("Importando librerías...")                                                # mensaje de control
from datetime import time, datetime
from business_duration import businessDuration
import holidays

#%%---------------------------- Variables globales -----------------------------
print("Preparando el sistema...")                                               # mensaje de control

#Business duration can be 'day', 'hour', 'min', 'sec'
unit ='sec'                                                                     # variable que especifica las unidades en que se quiere medir la duracion

holiday_list = holidays.CO()                                                    # se usa la libreria holidays para identificar los dias festivos en colombia

start_date = datetime.strptime('2022/05/09 8:00:05', '%Y/%m/%d %H:%M:%S')       # fecha inicio
end_date = datetime.strptime('2022/05/13 17:35:10', '%Y/%m/%d %H:%M:%S')        # fecha fin

biz_open_time=time(8,0,0)                                                       # hora inicio proceso (inicio tiempo de atencion del area) formato: (Hora,Minuto,Segundo)
biz_close_time=time(18,0,0)                                                     # hora fin proceso

#%%---------------------------- funciones y clases -----------------------------

def convert_seconds_to_time(total_seconds):
  """Convierte segundos a formato días:horas:minutos:segundos"""
  dias, remainder = divmod(total_seconds, 86400)  # 86400 segundos = 1 día
  horas, remainder = divmod(remainder, 3600)
  minutos, segundos = divmod(remainder, 60)
  return int(dias), int(horas), int(minutos), int(segundos)

def convert_time_to_seconds(horas, minutos, segundos):
  """Convierte horas:minutos:segundos a segundos totales"""
  return horas * 3600 + minutos * 60 + segundos

#-------------------------------- Main Function --------------------------------
def main():                             # Definicion de funcion principal
  duracion = businessDuration(startdate=start_date,
                              enddate=end_date,
                              starttime=biz_open_time,
                              endtime=biz_close_time,
                              holidaylist=holiday_list,
                              unit=unit)                                          # calculo de la duracion del tiempo de negocio

  # Convertir a formato legible
  dias, horas, minutos, segundos = convert_seconds_to_time(duracion)

  # Mostrar resultados
  print("=" * 50)
  print("RESULTADOS DEL CÁLCULO DE TIEMPO LABORAL")
  print("=" * 50)
  print(f"Duración en segundos: {duracion}")
  print(f"Formato compacto: {dias}d {horas:02d}:{minutos:02d}:{segundos:02d}")

  # Verificación: convertir de vuelta a segundos
  segundos_verificacion = convert_time_to_seconds(horas, minutos, segundos)
  print(f"Verificación (conversión a segundos): {segundos_verificacion}")

  # Ejemplo de operación con fechas
  print("\n" + "-" * 40)
  print("EJEMPLO DE OPERACIÓN CON FECHAS")
  print("-" * 40)

  format_hora = "%H:%M:%S"
  tiempo_calculado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
  tiempo_referencia = "2:00:00"

  x = datetime.strptime(tiempo_calculado, format_hora)
  y = datetime.strptime(tiempo_referencia, format_hora)
  diferencia = x - y

  print(f"Tiempo calculado: {tiempo_calculado}")
  print(f"Tiempo de referencia: {tiempo_referencia}")
  print(f"Diferencia: {diferencia}")
#--------------------------------- Run program ---------------------------------
if __name__ == "__main__":                                                      # condicion para ejecutar el programa (No ejecuta si se importa el script - puesto que este no seria el main script)
  main()                                                                        # llamado a la funcion principal del programa