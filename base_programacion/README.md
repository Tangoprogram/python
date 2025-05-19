# Base Programación
Plantilla base para iniciar proyectos Python de forma estructurada y profesional.

Incluye:
- El paquete reutilizable **fpack** con utilidades para archivos, interfaces gráficas, seguridad y automatización.
- Un archivo **plantilla.py**: script guía para estructurar nuevos programas, con buenas prácticas y manejo de errores.
- **requirements.txt**: dependencias externas necesarias para el paquete y scripts.
- **README.md**: documentación y guía de uso.

## Estructura del proyecto
```
base_programacion/
│
├── fpack/                # Paquete reutilizable (con __init__.py y módulos)
│   ├── __init__.py
│   ├── file_utils.py
│   ├── gui_utils.py
│   ├── security_utils.py
│   └── external_utils.py
│
├── plantilla.py          # Script plantilla para nuevos programas
├── requirements.txt      # Archivo de dependencias
├── README.md             # Documentación principal
└── (otros archivos: setup.py, pyproject.toml, tests/, etc.)
```

## ¿Cómo usar esta plantilla?
1. **Para crear un nuevo proyecto:**
   - Copia la carpeta `base_programacion` y renómbrala según tu proyecto.
   - Usa `plantilla.py` como base para tu script principal:
     Renómbralo y modifícalo según tus necesidades, manteniendo la estructura y buenas prácticas sugeridas.

2. **Para aprovechar el paquete `fpack`:**
   - Importa los módulos de `fpack` en tus scripts para acceder a utilidades de archivos, GUI, seguridad y automatización.
   - Consulta la sección de [Módulos y funcionalidades](#módulos-y-funcionalidades) para ver todo lo que ofrece.

3. **Para instalar dependencias:**

    Antes de usar el paquete, instala las dependencias externas ejecutando:

    ```bash
    pip install -r requirements.txt
    ```

    > **Nota:**
    > Las librerías estándar de Python (`os`, `sys`, `logging`, `tkinter`, etc.) **no requieren instalación** adicional.
    > El archivo `requirements.txt` solo incluye las librerías externas necesarias.

## Características principales de fpack
- **file_utils**: Funciones para manejo de archivos y datos, incluyendo protección de archivos Excel.
- **gui_utils**: Herramientas para crear interfaces gráficas dinámicas con botones configurables.
- **security_utils**: Funciones para manejo seguro de credenciales y bloqueo de scripts por contraseña.
- **external_utils**: Utilidades externas y soporte para integración con otras bibliotecas.

## Módulos y funcionalidades
### `file_utils`
Utilidades para la manipulación de archivos y datos, especialmente orientadas a Excel y DataFrames.

- **create_file(path, content):**
  Crea un archivo en la ruta especificada y escribe el contenido proporcionado.
- **remove_files(path):**
  Elimina todos los archivos dentro de una carpeta dada, útil para limpiar directorios temporales.
- **read_files(path, extensions=None, files=None, separator="|", header="infer", consolidate=False):**
  Lee archivos de una carpeta según extensiones o nombres específicos, y puede consolidarlos en un único DataFrame.
- **searchv(df, search_field, search_value, return_field=None):**
  Busca un valor en una columna de un DataFrame y retorna la fila o el campo solicitado.
- **protect_excel(file_path, sheet_name="Sheet1", password="frank", unlock_columns=None, protect_all_sheets=False):**
  Protege una hoja o todo el libro de Excel con contraseña, permitiendo desbloquear columnas específicas para edición.

### `gui_utils`
Herramientas para construir interfaces gráficas de usuario (GUI) de forma sencilla y flexible.

- **dynamicgui:**
  Clase principal para crear ventanas con botones personalizados.
  - Permite definir el título de la ventana y una lista de botones, cada uno con su acción asociada.
  - Métodos para centrar la ventana, gestionar errores, personalizar fuentes, colores y estilos.
  - Facilita la creación rápida de prototipos de interfaces sin necesidad de conocimientos avanzados de Tkinter.

### `security_utils`
Funciones y clases para la gestión segura de contraseñas y credenciales.

- **block(contraseña, max_attempts=3):**
  Bloquea la ejecución del script hasta que el usuario ingrese la contraseña correcta, con un número máximo de intentos.
- **credentialmanager:**
  Clase para almacenar y recuperar credenciales de forma segura.
  - Utiliza cifrado (Fernet) y almacenamiento seguro en el sistema (`keyring`).
  - Incluye interfaz gráfica para ingresar y gestionar credenciales.
  - Útil para automatizaciones que requieren acceso seguro a contraseñas o tokens.

### `external_utils`
Utilidades para la integración con servicios externos y automatización avanzada.

- **read_table(table_locator):**
  Extrae el contenido de una tabla HTML desde una página web usando Selenium, devolviendo los datos como lista de listas.
- **send_mail(subject, body, to, cc=None, bcc=None, attachments=None):**
  Envía correos electrónicos a través de Outlook, permitiendo adjuntar archivos y definir destinatarios en copia y copia oculta.
- **df_to_html(df):**
  Convierte un DataFrame de pandas en una tabla HTML, útil para reportes o correos electrónicos con formato.

## Documentación
Cada módulo y función incluye docstrings con ejemplos de uso y explicación de parámetros.

Puedes consultar la documentación directamente desde Python usando la función `help()`, inspeccionando el docstring, o viendo los nombres disponibles en un módulo.
Por ejemplo:

```python
import fpack.file_utils as fu
print(dir(fu))
print(fu.protect_excel.__doc__)
help(fu.protect_excel)
```
Consulta el código fuente para más detalles y ejemplos avanzados.

## Notas técnicas

- El paquete está diseñado para Python 3.9.12 o superior.
- Algunas funciones requieren Windows (por ejemplo, automatización de Outlook con `win32com.client`).
- Si usas funciones que requieren `tkinter`, asegúrate de tenerlo instalado (viene por defecto en la mayoría de instalaciones de Python).

## Créditos

- Autor: frposada
- Fecha de creación: 2025