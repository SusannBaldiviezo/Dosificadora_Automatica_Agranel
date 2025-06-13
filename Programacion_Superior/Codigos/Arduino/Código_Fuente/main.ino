#include "Dispensador.h"  

void setup() {
  // Inicialización de la comunicación serial
  Serial.begin(115200);
  // Configura sensores, LCD, pines y realiza tara inicial
  inicializarSistema();     
}

void loop() {
  // Lectura del peso actual
  float peso_actual = leerPeso();  
  
  enviarPorSerialPeriodicamente(peso_actual);  
  // Lectura de los botones físicos (UP, DOWN, START)
  manejarBotones();                            

  // Máquina de estados finita
  switch (estadoActual) {
    case CONFIGURACION:
      actualizarPantalla(peso_actual);  // Muestra peso actual y meta en la pantalla
      break;

    case ACTIVAR_MOTOR:
      mostrarMensaje("Sirviendo...", "");  
      beepInicio();                        // Sonido del buzzer que indica el inicio del proceso
      abrirServo();                        // Abre el servo para dispensar
      estadoActual = CONTROL_CANTIDAD;     // Cambia al siguiente estado
      break;

    case CONTROL_CANTIDAD:
      // Verifica si se alcanzó el umbral de peso
      if (peso_actual < peso_umbral - 10) {
        Serial.print("PROGRESO:");
        Serial.println(peso_actual, 1);
      } else {
        cerrarServo();                     // Cierra el servo al alcanzar el peso
        estadoActual = FINALIZACION;      // Cambia al estado final
      }
      break;

    case FINALIZACION:
      finalizarDispensado();              // Muestra mensaje, suena el buzzer para indicar la finalización del proceso, guarda el peso final y hace tara
      break;
  }

  leerComandosSerial();   // Revisa si llegaron comandos por el puerto serial (START, SET, TARE)

  delay(100);
}
