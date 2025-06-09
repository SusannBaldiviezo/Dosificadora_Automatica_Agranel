from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import serial
import serial.tools.list_ports
import threading
import time
from typing import Optional
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Control de Balanza")

# Configuración serial
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
RECONNECT_INTERVAL = 5  # segundos

# Estado del sistema
system_state = {
    "peso_actual": 0.0,
    "umbral": 100,
    "conectado": False,
    "logs": [],
    "ultimo_update": None
}

# Configuración del puerto serial
arduino = None
serial_thread = None
stop_threads = False

# Función para conectar al Arduino
def conectar_arduino():
    global arduino, system_state
    
    while not stop_threads:
        try:
            if arduino is None or not arduino.is_open:
                logger.info(f"Intentando conectar a {SERIAL_PORT}...")
                
                # Listar puertos disponibles para diagnóstico
                ports = serial.tools.list_ports.comports()
                logger.info(f"Puertos disponibles: {[p.device for p in ports]}")
                
                arduino = serial.Serial(
                    port=SERIAL_PORT,
                    baudrate=BAUD_RATE,
                    timeout=1,
                    write_timeout=1
                )
                time.sleep(2)  # Esperar inicialización
                system_state["conectado"] = True
                logger.info("Conexión establecida con Arduino")
                
        except Exception as e:
            system_state["conectado"] = False
            logger.error(f"Error de conexión: {str(e)}")
            if arduino:
                arduino.close()
                arduino = None
            time.sleep(RECONNECT_INTERVAL)

# Función para leer datos del serial
def leer_serial():
    global system_state
    
    while not stop_threads:
        try:
            if arduino and arduino.is_open:
                if arduino.in_waiting:
                    linea = arduino.readline().decode('utf-8').strip()
                    if linea:
                        procesar_linea_serial(linea)
        except Exception as e:
            logger.error(f"Error leyendo serial: {str(e)}")
            system_state["conectado"] = False
            time.sleep(1)

def procesar_linea_serial(linea: str):
    global system_state
    
    # Mantener registro de logs
    system_state["logs"].append(linea)
    if len(system_state["logs"]) > 100:
        system_state["logs"] = system_state["logs"][-100:]
    
    logger.info(f"Dato recibido: {linea}")
    
    # Procesar diferentes tipos de mensajes
    if linea.startswith("PESO:"):
        try:
            peso = float(linea.split(":")[1])
            system_state["peso_actual"] = peso
            system_state["ultimo_update"] = time.time()
        except (IndexError, ValueError) as e:
            logger.warning(f"Error procesando peso: {str(e)}")
    
    elif linea.startswith("Umbral actualizado:"):
        try:
            umbral = int(linea.split(":")[1])
            system_state["umbral"] = umbral
        except (IndexError, ValueError) as e:
            logger.warning(f"Error procesando umbral: {str(e)}")

# Eventos de inicio/parada
@app.on_event("startup")
def iniciar_sistema():
    global serial_thread
    
    # Hilo para conexión serial
    threading.Thread(target=conectar_arduino, daemon=True).start()
    
    # Hilo para lectura de datos
    serial_thread = threading.Thread(target=leer_serial, daemon=True)
    serial_thread.start()
    
    logger.info("Sistema iniciado")

@app.on_event("shutdown")
def detener_sistema():
    global stop_threads, arduino
    
    stop_threads = True
    if arduino and arduino.is_open:
        arduino.close()
    
    logger.info("Sistema detenido")

# Endpoints de la API
@app.get("/", response_class=HTMLResponse)
def interfaz_web():
    return f"""
    <html>
        <head>
            <title>Sistema de Balanza</title>
            <meta http-equiv="refresh" content="1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .panel {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .data-display {{ font-size: 1.5em; margin: 10px 0; }}
                .connected {{ color: green; }}
                .disconnected {{ color: red; }}
                .logs {{ max-height: 200px; overflow-y: auto; background: #333; color: #fff; padding: 10px; }}
                button {{ padding: 8px 16px; margin-right: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Sistema de Control de Balanza</h1>
                
                <div class="panel">
                    <h2>Estado del Sistema</h2>
                    <p>Conexión: 
                        <span class="{'connected' if system_state['conectado'] else 'disconnected'}">
                            {'✅ Conectado' if system_state['conectado'] else '❌ Desconectado'}
                        </span>
                    </p>
                    
                    <div class="data-display">
                        <strong>Peso actual:</strong> {system_state['peso_actual']:.1f} g
                    </div>
                    
                    <div class="data-display">
                        <strong>Umbral actual:</strong> {system_state['umbral']} g
                    </div>
                    
                    <div>
                        <button onclick="fetch('/iniciar', {{method: 'POST'}})">Iniciar Servido</button>
                    </div>
                </div>
                
                <div class="panel">
                    <h2>Ajustar Umbral</h2>
                    <form onsubmit="event.preventDefault(); ajustarUmbral()">
                        <input type="number" id="umbral" min="100" max="5000" value="{system_state['umbral']}">
                        <button type="submit">Actualizar</button>
                    </form>
                </div>
                
                <div class="panel">
                    <h2>Registro de Eventos</h2>
                    <div class="logs">
                        {"<br>".join(system_state['logs'][-10:])}
                    </div>
                </div>
            </div>
            
            <script>
                function ajustarUmbral() {{
                    const valor = document.getElementById('umbral').value;
                    fetch(/umbral?valor=${{valor}}, {{method: 'POST'}})
                        .then(response => response.json())
                        .then(data => console.log(data));
                }}
            </script>
        </body>
    </html>
    """

@app.get("/api/peso")
def obtener_peso():
    if not system_state["conectado"]:
        raise HTTPException(status_code=503, detail="Arduino no conectado")
    return {
        "peso": round(system_state["peso_actual"], 1),
        "unidad": "g",
        "timestamp": system_state["ultimo_update"]
    }

@app.get("/api/logs")
def obtener_logs(limit: int = Query(10, ge=1, le=100)):
    return {
        "logs": system_state["logs"][-limit:],
        "total": len(system_state["logs"])
    }

@app.post("/api/umbral")
def ajustar_umbral(valor: int = Query(..., ge=100, le=5000)):
    if not system_state["conectado"]:
        raise HTTPException(status_code=503, detail="Arduino no conectado")
    
    try:
        if arduino and arduino.is_open:
            arduino.write(f"SET:{valor}\n".encode())
            system_state["umbral"] = valor
            return {"status": "success", "nuevo_umbral": valor}
    except Exception as e:
        logger.error(f"Error enviando umbral: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al enviar comando")
    
    return {"status": "error", "message": "No se pudo enviar el comando"}

@app.post("/api/iniciar")
def iniciar_proceso():
    if not system_state["conectado"]:
        raise HTTPException(status_code=503, detail="Arduino no conectado")
    
    try:
        if arduino and arduino.is_open:
            arduino.write(b"START\n")
            return {"status": "success", "message": "Comando enviado"}
    except Exception as e:
        logger.error(f"Error iniciando proceso: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al iniciar proceso")
    
    return {"status": "error", "message": "No se pudo enviar el comando"}
