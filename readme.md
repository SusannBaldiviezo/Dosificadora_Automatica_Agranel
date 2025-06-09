
Requisitos del Sistema
==========================
Hardware necesario:

    Arduino Nano con el sketch proporcionado cargado

    Módulo HX711 para la celda de carga

    Servomotor (SG90 o similar)

    Display LCD I2C (16x2 caracteres)

    3 botones (para control manual)

    Buzzer/LED para feedback

    Celda de carga (con capacidad adecuada)

    Cables de conexión

Software necesario:

    Python 3.7 o superior

    FastAPI y Uvicorn

    PySerial

    Navegador web moderno
==========================

Instalación y Configuración
1. Instalar dependencias Python:
pip install fastapi uvicorn pyserial

2. Configurar el puerto serial:
En el archivo main.py, modifica esta línea con el puerto correcto:
SERIAL_PORT = "COM3"  
# Cambiar por el puerto correcto (COM6, COM4, etc.)
3. Conectar el hardware:
Conecta el Arduino Nano al puerto USB de la computadora
Verifica que todos los componentes estén correctamente conectados según el diagrama
==========================
Ejecución del Sistema
Opción 1: Desde línea de comandos
uvicorn main:app --reload
Opción 2: Desde Visual Studio Code

    Abre el proyecto en VS Code

    Abre la terminal integrada (Ctrl+`)

    Ejecuta el comando:
    uvicorn main:app --reload
==========================  
Acceso a la interfaz:
http://127.0.0.1:8000/