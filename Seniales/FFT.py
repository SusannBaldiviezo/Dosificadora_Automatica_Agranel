import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


datos = pd.read_csv('datos_peso.csv')  
x = datos['peso']


fs = 10  
fc = 1  
w = fc / (fs / 2)  
b, a = butter(4, w, 'low')  


xfiltrada = lfilter(b, a, x)


X = np.fft.fft(x)
frecuencias = np.fft.fftfreq(len(x), 1/fs)

plt.figure()
plt.plot(x)
plt.title("Señal original de peso")
plt.xlabel("Muestras")
plt.ylabel("Peso")
plt.grid()
plt.show()


plt.figure()
plt.plot(frecuencias, np.abs(X))
plt.title("FFT de la señal original")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Magnitud")
plt.grid()
plt.xlim(0, fs/2)
plt.show()


plt.figure()
plt.plot(x, label="Original", alpha=0.5)
plt.plot(xfiltrada, label="Filtrada", linewidth=2)
plt.title("Señal de peso filtrada")
plt.xlabel("Muestras")
plt.ylabel("Peso")
plt.legend()
plt.grid()
plt.show()
