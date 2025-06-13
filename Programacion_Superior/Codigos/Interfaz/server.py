from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
import serial
import serial.tools.list_ports
import threading
import time
from typing import Optional
import logging
from datetime import datetime

app = FastAPI()

# Configuración
PORT = "COM6"
BAUD_RATE = 115200
RECONNECT_INTERVAL = 5

# Estado del sistema
system_state = {
    "peso_actual": 0.0,
    "peso_umbral": 100,
    "conectado": False,
    "dispensaciones": [],
    "total_inicial": 1000.0,
    "total_restante": 1000.0,
    "ultimo_update": None
}

arduino = None
stop_threads = False

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def conectar_arduino():
    global arduino, system_state
    while not stop_threads:
        try:
            if arduino is None or not arduino.is_open:
                logger.info(f"Conectando a {PORT}...")
                arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
                system_state["conectado"] = True
                logger.info("Conexión establecida")
                time.sleep(2)
        except Exception as e:
            system_state["conectado"] = False
            logger.error(f"Error de conexión: {str(e)}")
            if arduino:
                arduino.close()
                arduino = None
            time.sleep(RECONNECT_INTERVAL)

def leer_serial():
    global system_state
    while not stop_threads:
        try:
            if arduino and arduino.is_open:
                if arduino.in_waiting:
                    linea = arduino.readline().decode('utf-8').strip()
                    procesar_mensaje(linea)
        except Exception as e:
            logger.error(f"Error serial: {str(e)}")
            system_state["conectado"] = False
            time.sleep(1)

def procesar_mensaje(mensaje: str):
    global system_state
    
    if not mensaje:
        return
        
    logger.info(f"Dato recibido: {mensaje}")
    system_state["ultimo_update"] = time.time()
    
    if mensaje.startswith("PESO:"):
        try:
            peso = float(mensaje[5:])
            system_state["peso_actual"] = peso
        except ValueError as e:
            logger.error(f"Error procesando peso: {str(e)}")
    
    elif mensaje.startswith("UMBRAL:"):
        try:
            umbral = int(mensaje[7:])
            system_state["peso_umbral"] = umbral
        except ValueError as e:
            logger.error(f"Error procesando umbral: {str(e)}")
    
    elif mensaje.startswith("FINAL:"):
        try:
            peso_final = float(mensaje[6:])
            # Actualizamos el peso actual
            system_state["peso_actual"] = peso_final
        except ValueError as e:
            logger.error(f"Error procesando final: {str(e)}")
    
    elif mensaje.startswith("DISPENSADO:"):
        try:
            peso_dispensado = float(mensaje[11:])
            registrar_dispensacion(peso_dispensado)
        except ValueError as e:
            logger.error(f"Error procesando dispensado: {str(e)}")
    
    elif mensaje == "TARE:OK":
        logger.info("Tara realizada correctamente")
        system_state["peso_actual"] = 0.0

def registrar_dispensacion(peso_dispensado: float):
    global system_state
    
    # Actualizamos el total restante
    system_state["total_restante"] -= peso_dispensado
    
    # Registramos la dispensación
    system_state["dispensaciones"].append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "peso": peso_dispensado,
        "restante": system_state["total_restante"]
    })
    
    # Mantener solo últimas 20
    if len(system_state["dispensaciones"]) > 20:
        system_state["dispensaciones"] = system_state["dispensaciones"][-20:]

@app.on_event("startup")
def iniciar_sistema():
    threading.Thread(target=conectar_arduino, daemon=True).start()
    threading.Thread(target=leer_serial, daemon=True).start()
    logger.info("Sistema iniciado")

@app.on_event("shutdown")
def detener_sistema():
    global stop_threads, arduino
    stop_threads = True
    if arduino and arduino.is_open:
        arduino.close()
    logger.info("Sistema detenido")

@app.get("/", response_class=HTMLResponse)
def interfaz_web():
    tabla = "".join(
        f"<tr><td>{d['timestamp']}</td>"
        f"<td>{d['peso']:.1f}g</td><td>{d['restante']:.1f}g</td></tr>"
        for d in reversed(system_state["dispensaciones"][-10:])
    )
    
    return f"""
    <html>
        <head>
            <title>Sistema de Balanza</title>
            <meta http-equiv="refresh" content="1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .status {{ 
                    padding: 10px; 
                    background: {'#f8d7da' if not system_state['conectado'] else '#d4edda'}; 
                    color: {'#721c24' if not system_state['conectado'] else '#155724'};
                    margin-bottom: 20px; 
                    border-radius: 5px;
                }}
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 20px; 
                }}
                th, td {{ 
                    padding: 8px; 
                    text-align: left; 
                    border-bottom: 1px solid #ddd; 
                }}
                .data-display {{ 
                    margin: 10px 0; 
                    padding: 10px;
                    background: #f0f0f0;
                    border-radius: 5px;
                }}
                button {{
                    padding: 10px 15px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }}
                button:hover {{
                    background: #0056b3;
                }}
                .button-danger {{
                    background: #dc3545;
                }}
                .button-danger:hover {{
                    background: #c82333;
                }}
                .button-success {{
                    background: #28a745;
                }}
                .button-success:hover {{
                    background: #218838;
                }}
            </style>
        </head>
        <body>
            <h1>Sistema de Control de Balanza</h1>
            
            <div class="status">
                Estado: {'❌ DESCONECTADO' if not system_state['conectado'] else '✅ CONECTADO'}
            </div>
            
            <div class="data-display">
                <strong>Peso actual:</strong> {system_state['peso_actual']:.1f}g
            </div>
            
            <div class="data-display">
                <strong>Umbral actual:</strong> {system_state['peso_umbral']}g
            </div>
            
            <div class="data-display">
                <strong>Total restante:</strong> {system_state['total_restante']:.1f}g
            </div>
            
            <div>
                <button onclick="iniciarServido()" class="button-success">Iniciar Servido</button>
                <button onclick="actualizarUmbral()">Cambiar Umbral</button>
                <button onclick="hacerTara()" class="button-success">Hacer Tara</button>
                <button onclick="resetearSistema()" class="button-danger">Resetear Sistema</button>
            </div>
            
            <h2>Historial de Dispensaciones</h2>
            <table>
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Peso Dispensado</th>
                        <th>Total Restante</th>
                    </tr>
                </thead>
                <tbody>
                    {tabla}
                </tbody>
            </table>
            
            <script>
                async function iniciarServido() {{
                    const response = await fetch('/iniciar', {{method: 'POST'}});
                    const data = await response.json();
                    alert(data.message);
                }}
                
                async function actualizarUmbral() {{
                    const nuevoUmbral = prompt('Ingrese nuevo umbral (100-5000g):', {system_state['peso_umbral']});
                    if (nuevoUmbral && !isNaN(nuevoUmbral)) {{
                        const response = await fetch(`/umbral?valor=${{nuevoUmbral}}`, {{method: 'POST'}});
                        const data = await response.json();
                        alert(data.message || 'Umbral actualizado');
                    }}
                }}
                
                async function hacerTara() {{
                    const confirmar = confirm('¿Está seguro que desea hacer tara? Esto reseteará el peso actual a 0');
                    if (confirmar) {{
                        const response = await fetch('/tara', {{method: 'POST'}});
                        const data = await response.json();
                        alert(data.message);
                    }}
                }}
                
                async function resetearSistema() {{
                    const confirmar = confirm('¿Está seguro de resetear el sistema? Esto pondrá el total restante a 1000g');
                    if (confirmar) {{
                        const response = await fetch('/reset', {{method: 'POST'}});
                        const data = await response.json();
                        alert(data.message);
                    }}
                }}
            </script>
        </body>
    </html>
    """

@app.post("/iniciar")
def iniciar_servido():
    if not system_state["conectado"]:
        raise HTTPException(status_code=400, detail="Arduino no conectado")
    
    try:
        arduino.write(b"START\n")
        return {"message": "Comando de inicio enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/umbral")
def ajustar_umbral(valor: int = Query(..., ge=100, le=5000)):
    if not system_state["conectado"]:
        raise HTTPException(status_code=400, detail="Arduino no conectado")
    
    try:
        arduino.write(f"SET:{valor}\n".encode())
        system_state["peso_umbral"] = valor
        return {"message": f"Umbral actualizado a {valor}g"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tara")
def hacer_tara():
    if not system_state["conectado"]:
        raise HTTPException(status_code=400, detail="Arduino no conectado")
    
    try:
        arduino.write(b"TARE\n")
        system_state["peso_actual"] = 0.0
        return {"message": "Comando de tara enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
def resetear_sistema():
    try:
        # Enviamos comando de tara al Arduino
        if system_state["conectado"]:
            arduino.write(b"TARE\n")
        
        # Resetear estado del sistema
        system_state["total_restante"] = system_state["total_inicial"]
        system_state["dispensaciones"] = []
        system_state["peso_actual"] = 0.0
        
        return {"message": "Sistema reseteado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))