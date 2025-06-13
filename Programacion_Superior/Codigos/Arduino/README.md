# 🟦 Sistema de Dosificación con Balanza Digital para Arduino

Este proyecto implementa un sistema de **dosificación automática mediante una balanza digital**, controlado por un microcontrolador Arduino y actuado por un servomotor. El sistema se apoya en una interfaz de pantalla LCD y un conjunto de botones físicos para interactuar con el usuario.

---

## ⚙️ Componentes del Sistema

- 📟 **Pantalla LCD I2C**  
  Muestra el estado actual del sistema y los datos de pesaje.
  
- ⚖️ **Celda de carga + Módulo HX711**  
  Permite medir el peso del contenido para una dosificación precisa.

- 🔘 **Botones de control**  
  - `UP`: para aumentar el peso deseado.  
  - `DOWN`: para disminuirlo.  
  - `START`: para iniciar la dosificación.  
  - `SET`: para confirmar configuraciones.

- 🔄 **Servomotor**  
  Activa el mecanismo de dosificación abriendo/cerrando una compuerta o válvula.

- 🔔 **Zumbador (Buzzer)**  
  Emite alertas sonoras durante el proceso.

---

## 🔄 Funcionamiento General

El sistema opera bajo una lógica basada en **máquina de estados**, donde cada fase del proceso está claramente definida:

1. **CONFIGURACIÓN**  
   El usuario selecciona la cantidad deseada de producto a dispensar utilizando los botones físicos. Esta cantidad se muestra en la pantalla LCD.

2. **ACTIVAR_MOTOR**  
   Una vez confirmado el valor, se activa el servomotor para iniciar la dosificación del producto.

3. **CONTROL_CANTIDAD**  
   La balanza mide en tiempo real el peso dispensado. El sistema compara esta lectura con la cantidad objetivo.  
   Si aún no se alcanza, continúa la dosificación.

4. **FINALIZACIÓN**  
   Al alcanzar el peso programado, el servomotor se detiene y se notifica al usuario mediante el buzzer y la pantalla LCD.

---

## 🔋 Recomendaciones

- Calibrar correctamente la celda de carga utilizando el valor `FACTOR_CALIBRACION` adecuado a tu sensor HX711.
- Usar una fuente de alimentación externa si se conecta una carga mecánica al servomotor.
- Asegurarse de que los cables del módulo de peso estén bien conectados (E+, E−, A+, A−).

---

## 📁 Archivos Relevantes

- `.ino`: Archivo principal de Arduino que contiene `setup()` y `loop()`.
- `.cpp`: Lógica completa del funcionamiento y gestión de hardware.
- `.h`: Declaración de estados del sistema y funciones públicas del controlador.

---

## 🛠️ Librerías utilizadas

- `LiquidCrystal_I2C`: Para la pantalla LCD.
- `HX711`: Para la lectura del módulo de pesaje.
- `Servo`: Para el control del servomotor.

---

## ✅ Estado del Proyecto

✔️ Estable y funcional. Listo para integrarse a sistemas de dosificación por peso como:
- Máquinas dispensadoras de granos.  
- Proyectos de automatización agrícola o alimentaria.  
- Control de porciones en cocina o laboratorios.

---



---

Desarrollado con ❤ por Susann Baldiviezo, Florencia Frigerio, Jesus Ibarra, Giovanna Tarifa
