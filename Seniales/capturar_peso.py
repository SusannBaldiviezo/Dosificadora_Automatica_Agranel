import serial
import time
import pandas as pd
import matplotlib.pyplot as plt

puerto = 'COM3'  # ⚠️ CAMBIA esto según tu PC (puede ser COM4, /dev/ttyUSB0 en Linux, etc.)
baudrate = 9600
tiempo_muestreo = 10  # segundos

datos = []

# Abrir puerto serial
with serial.Serial(puerto, baudrate, timeout=1) as arduino:
    print("Conectado a", puerto)
    inicio = time.time()
    
    while time.time() - inicio < tiempo_muestreo:
        linea = arduino.readline().decode('utf-8').strip()
        try:
            peso = float(linea)
            datos.append(peso)
            print(peso)
        except:
            pass

# Guardar en CSV
df = pd.DataFrame(datos, columns=["Peso (g)"])
df.to_csv("datos_peso.csv", index=False)
print("Datos guardados en datos_peso.csv")

# Graficar
plt.plot(df["Peso (g)"])
plt.title("Señal de peso en el tiempo")
plt.xlabel("Muestras")
plt.ylabel("Peso (gramos)")
plt.grid()
plt.show()
