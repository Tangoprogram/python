@echo off

:: Verifica si el entorno virtual existe
if not exist C:\.venv (
    echo Creando el entorno virtual...
    python -m venv C:\.venv
)

:: Activa el entorno virtual
call C:\.venv\Scripts\activate

:: Actualiza pip
pip install --upgrade pip

:: Cambia al directorio donde están los archivos (ajusta la ruta según sea necesario)
pushd "C:\Users\frposada\Music"

:: Instala las librerías desde el archivo requirements.txt
if exist requirements.txt (
    echo Instalando las librerías del archivo requirements.txt...
    pip install -r requirements.txt
) else (
    echo No se encontró el archivo requirements.txt, por lo que no se instalarán dependencias.
)

:: Ejecuta el script Python
if exist script.py (
    echo Ejecutando script.py...
    python script.py
) else (
    echo No se encontró script.py.
)

:: Desactiva el entorno virtual
call C:\.venv\Scripts\deactivate

pause