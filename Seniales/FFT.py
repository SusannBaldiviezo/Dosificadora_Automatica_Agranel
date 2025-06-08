import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("datos_peso.csv")
datos = df["Peso (g)"].values


N = len(datos)
Fs = 10 
T = 1 / Fs
frecuencia = np.fft.fftfreq(N, T)
espectro = np.fft.fft(datos)
magnitud = np.abs(espectro)


plt.figure()
plt.plot(frecuencia[:N//2], magnitud[:N//2]) 
plt.title("Espectro de frecuencia de la señal de peso")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.grid()
plt.show()
