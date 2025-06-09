#include "modulos/fsm.h"
#include "modulos/balance.h"
#include "modulos/botones.h"
#include "modulos/servo.h"
#include "modulos/buzzer.h"
#include "modulos/pantalla.h"

// Estado actual
Estado estadoActual;

void setup() {
  // Inicialización de módulos
  Serial.begin(9600);

  inicializarBotones();
  inicializarServo();
  inicializarBuzzer();
  inicializarBalance();
  inicializarPantalla();

  // Mostrar mensaje inicial
  mostrarBienvenida();

  // Estado inicial
  estadoActual = INICIO;
}

void loop() {
  // Ejecuta la máquina de estados
  estadoActual = ejecutarFSM(estadoActual);
  
  delay(100); // Pequeño retardo para evitar sobrecarga
}
