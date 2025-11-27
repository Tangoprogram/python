"""
permite identificar fotos duplicadas en una carpeta y
brinda un interfaz al usuario para decidir si eliminar o no las imagenes duplicadas
"""

import os                                                                       # Biblioteca para interactuar con el sistema operativo
import imagehash                                                                # Biblioteca para calcular hashes de imágenes, Un hash perceptual es un valor que representa el contenido visual de una imagen y permite comparar imágenes de manera eficiente para determinar si son similares
from PIL import Image, ImageTk                                                  # Módulos de PIL (Pillow) para manejar imágenes y su visualización
from collections import defaultdict                                             # Estructura de datos defaultdict para manejar listas por defecto
import tkinter as tk                                                            # Biblioteca para construir interfaces gráficas (GUI)
from tkinter import messagebox, simpledialog                                    # Componentes específicos de tkinter para manejar mensajes y diálogos

def find_duplicate_images(folder_path):
    """
    Encuentra imágenes duplicadas en una carpeta dada.

    Args:
    - folder_path (str): Ruta de la carpeta a explorar.

    Returns:
    - list: Lista de listas de rutas de archivos duplicados.
    """
    image_hashes = defaultdict(list)                                            # Diccionario para almacenar hashes de imágenes y sus rutas
    duplicates = []                                                             # Lista para almacenar grupos de imágenes duplicadas

    # Recorrer todos los archivos en la carpeta especificada
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff')): # condicion para determinar si el archivo es una imagen en sus diferentes formatos
            filepath = os.path.join(folder_path, filename)                      # concatena la ruta con el nombre del archivo para obtener la ruta del archivo
            try:
                # Abrir la imagen y calcular su hash perceptual
                image = Image.open(filepath)                                    # abre la imagen
                hash_value = imagehash.average_hash(image)                      # obtiene el hash de la imagen
                image_hashes[hash_value].append(filepath)                       # Agrupar por hash perceptual
            except Exception as e:
                print(f"Error al procesar {filepath}: {e}")

    # Encontrar grupos de imágenes duplicadas (más de una con el mismo hash)
    for hash_value, files in image_hashes.items():
        if len(files) > 1:
            duplicates.append(files)                                            # Agregar grupo de rutas duplicadas a la lista de resultados

    return duplicates

def show_next_group(duplicates, index=0):
    """
    Muestra el siguiente grupo de imágenes duplicadas en una ventana y permite al usuario decidir si eliminarlas.

    Args:
    - duplicates (list): Lista de listas de rutas de archivos duplicados.
    - index (int): Índice del grupo de imágenes duplicadas a mostrar.
    """
    if index >= len(duplicates):                                                # condicion para determinar si hay mas imagenes duplicadas
        messagebox.showinfo("Fin", "No hay más imágenes duplicadas.")
        root.quit()                                                             # Terminar el bucle principal de tkinter al finalizar el procesamiento
        return

    group = duplicates[index]                                                   # Obtener el grupo de imágenes duplicadas actual

    window = tk.Toplevel()                                                      # Crear una nueva ventana de tkinter
    window.title("Imágenes duplicadas encontradas")                             # Título de la ventana
    window.geometry("+%d+%d" % (window.winfo_screenwidth() // 2 - 200, window.winfo_screenheight() // 2 - 150))  # Centrar la ventana en la pantalla

    frame = tk.Frame(window)                                                    # Crear un marco dentro de la ventana
    frame.pack(padx=10, pady=10, fill="both", expand=True)                      # Añadir relleno al marco para mejor apariencia

    images_frame = tk.Frame(frame)                                              # Crear un sub-marco para las imágenes
    images_frame.pack(pady=20)                                                  # Empaquetar el sub-marco con un poco de relleno vertical

    images = []                                                                 # vector vacio para almacenar las imagenes
    for filepath in group:                                                      # ciclo para recorrer las imagenes dentro de los grupos de imagenes repetidas
        # Abrir la imagen y ajustar su tamaño para mostrar miniaturas
        image = Image.open(filepath)                                            # abrir imagen
        image.thumbnail((200, 100))                                             # Redimensionar la imagen a 100x100 píxeles
        img = ImageTk.PhotoImage(image)                                         # Convertir la imagen para usarla en tkinter
        images.append((img, filepath))                                          # Guardar la imagen convertida y su ruta

    for img, filepath in images:
        panel = tk.Label(images_frame, image=img)                                      # Crear un panel con la imagen dentro del marco
        panel.pack(side="left", padx=5, pady=5)                                 # Añadir el panel al marco con relleno

    def on_decision(decision):
        """
        Función para manejar la decisión del usuario de eliminar o no las imágenes duplicadas.

        Args:
        - decision (bool): True si el usuario decide eliminar, False si no.
        """
        if decision:                                                            # condicion para identificar si la decision del usuario es elimar las repetidas
            for img, filepath in images[1:]:                                    # ciclo para recorrer las imagenes del grupo
                try:
                    os.remove(filepath)                                         # Eliminar los archivos duplicados (excepto el primero)
                    print(f"{filepath} eliminado.")
                except Exception as e:
                    print(f"No se pudo eliminar {filepath}: {e}")
        window.destroy()                                                        # Cerrar la ventana actual después de tomar la decisión
        show_next_group(duplicates, index + 1)                                  # Mostrar el siguiente grupo de imágenes duplicadas

    question_label = tk.Label(frame, text="¿Deseas eliminar todas excepto una?") # Etiqueta de la pregunta
    question_label.pack(side="left", padx=5, pady=5)                                                       # Añadir la etiqueta al marco

    # Botones para "Sí" y "No" con sus respectivas funciones de decisión
    yes_button = tk.Button(frame, text="Sí", command=lambda: on_decision(True))
    yes_button.pack(side="left", padx=5, pady=5)                                # Añadir el botón "Sí" al marco

    no_button = tk.Button(frame, text="No", command=lambda: on_decision(False))
    no_button.pack(side="left", padx=5, pady=5)                                 # Añadir el botón "No" al marco

def display_and_decide(duplicates):
    """
    Función principal para mostrar grupos de imágenes duplicadas y permitir al usuario decidir sobre ellas.

    Args:
    - duplicates (list): Lista de listas de rutas de archivos duplicados.
    """
    global root
    root = tk.Tk()                                                              # Crear la ventana principal de tkinter
    root.withdraw()                                                             # Ocultar la ventana principal para mostrar solo las ventanas secundarias

    show_next_group(duplicates)                                                 # Mostrar el primer grupo de imágenes duplicadas

    root.mainloop()                                                             # Iniciar el bucle principal de tkinter para manejar eventos de la GUI

if __name__ == "__main__":
    folder_path = simpledialog.askstring("Ruta de la carpeta", "Introduce la ruta de la carpeta:") # Diálogo para obtener la ruta de la carpeta
    if folder_path:
        duplicates = find_duplicate_images(folder_path)                         # Buscar imágenes duplicadas en la carpeta especificada
        if duplicates:
            display_and_decide(duplicates)                                      # Mostrar y permitir al usuario decidir sobre los grupos de imágenes duplicadas encontradas
        else:
            messagebox.showinfo("Resultado", "No se encontraron imágenes duplicadas.") # Mensaje si no se encontraron duplicados