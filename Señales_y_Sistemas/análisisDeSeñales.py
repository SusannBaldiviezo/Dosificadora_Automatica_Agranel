import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import numpy as np
from scipy.signal import butter, filtfilt, tf2zpk

# Puerto serial
puerto = serial.Serial("COM3", 115200, timeout=1) #/dev/ttyUSB0 (Dependiendo si se ejecuta desde Windows o Linux)

# Declaración de variables
tiempos = []
pesos = []
inicio = None
inicio_registrado = False
mostro_polos_ceros = False  # Para mostrar polos y ceros solo una vez

# Inicialización de gráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Análisis temporal y comparación de la señal filtrada
linea_original, = ax1.plot([], [], 'r-', label='Original')
linea_filtrada, = ax1.plot([], [], 'g-', label='Filtrada Butterworth')
ax1.set_title("Análisis temporal")
ax1.set_xlabel("Tiempo (s)")
ax1.set_ylabel("Peso (g)")
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 1000)
ax1.grid(True)
ax1.legend()

# Análisis frecuencial (Gráfico FFT)
fft_linea, = ax2.plot([], [], 'b-')
ax2.set_title("Análisis frecuencial (FFT)")
ax2.set_xlabel("Frecuencia (Hz)")
ax2.set_ylabel("Magnitud")
ax2.set_xlim(0, 5)
ax2.set_ylim(0, 1000)
ax2.grid(True)

fs = 2  # Frecuencia de muestreo aproximada en Hz

# Diseño filtro Butterworth pasabajos (Filtro Digital IIR)
orden = 3
fc = 0.5
w = fc / (fs / 2)  # Normalizar frecuencia de corte

b, a = butter(orden, w, btype='low')


#Para los polos y ceros
def plot_poles_zeros(b, a, title):
    z, p, k = tf2zpk(b, a)
    plt.figure(figsize=(6, 6))
    plt.scatter(np.real(z), np.imag(z), marker='o', facecolors='none', edgecolors='b', label='Ceros')
    plt.scatter(np.real(p), np.imag(p), marker='x', color='r', label='Polos')
    plt.xlabel('Parte Real')
    plt.ylabel('Parte Imaginaria')
    plt.title(title)
    plt.grid(True)
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)
    plt.legend()
    plt.axis('equal')
    plt.show()

#Recoleción de datos en tiempo real en el estado de dispensión
def update(frame):
    global inicio, inicio_registrado, mostro_polos_ceros

    if puerto.in_waiting:
        linea_serial = puerto.readline().decode(errors='ignore').strip() #Lectura del peso
        print("DEBUG:", linea_serial)

        if linea_serial.startswith("PROGRESO:"):
            try:
                peso = float(linea_serial.split(":")[1])

                # Iniciar el tiempo cuando empieza el dispensado
                if not inicio_registrado:
                    inicio = time.time()
                    inicio_registrado = True
                    tiempos.clear()
                    pesos.clear()

                # Mostrar polos y ceros solo la primera vez que inicie dispensado
                if inicio_registrado and not mostro_polos_ceros:
                    plot_poles_zeros(b, a, "Polos y Ceros - Filtro IIR Butterworth pasabajo")
                    mostro_polos_ceros = True

                t = time.time() - inicio
                tiempos.append(t)
                pesos.append(peso)

                # Filtrado con Butterworth (si hay suficientes datos)
                pesos_filtrados = []
                if len(pesos) >= orden * 3:
                    pesos_filtrados = filtfilt(b, a, pesos)
                else:
                    pesos_filtrados = pesos  # Sin filtrar si hay pocos datos

                # Actualiza gráfica temporal
                linea_original.set_data(tiempos, pesos)
                linea_filtrada.set_data(tiempos, pesos_filtrados)
                ax1.set_xlim(max(0, t - 10), t + 1)
                ymax = max(max(pesos), max(pesos_filtrados))
                ax1.set_ylim(0, ymax + 100)

                # Análisis frecuencial usando señal original
                if tiempos[-1] - tiempos[0] >= 2 and len(pesos) >= 8:
                    idx_inicio = 0
                    for i, tiempo in enumerate(tiempos):
                        if tiempo >= tiempos[-1] - 2:
                            idx_inicio = i
                            break
                    datos_f = pesos[idx_inicio:]
                    n = len(datos_f)

                    fft_vals = np.fft.fft(datos_f)
                    fft_freq = np.fft.fftfreq(n, d=1/fs)

                    idx_pos = fft_freq >= 0
                    fft_freq = fft_freq[idx_pos]
                    fft_mag = np.abs(fft_vals[idx_pos])

                    fft_linea.set_data(fft_freq, fft_mag)
                    ax2.set_xlim(0, max(fft_freq))
                    ax2.set_ylim(0, max(fft_mag) * 1.1)

            except ValueError:
                print("Error al convertir el peso:", linea_serial)

    return linea_original, linea_filtrada, fft_linea

ani = FuncAnimation(fig, update, interval=200)
plt.tight_layout()
plt.show()
puerto.close()
