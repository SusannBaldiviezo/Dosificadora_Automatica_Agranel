#include "HX711.h"

HX711 balanza;

const float FACTOR_CALIBRACION = 432.802093;  

unsigned long tiempoAnterior = 0;
const unsigned long intervalo = 100; 

typedef enum {
  MODO_MANUAL,
  MODO_WEB,
  MODO_ANALISIS
} Estado;

Estado estadoActual = MODO_ANALISIS;  

void setup() {
  Serial.begin(9600);
  balanza.begin(5, 6); 
  balanza.set_scale(FACTOR_CALIBRACION);
  balanza.tare(); 
}

void loop() {
  switch (estadoActual) {
    case MODO_ANALISIS:
      modoAnalisis();
      break;
    case MODO_MANUAL:
   
      break;
    case MODO_WEB:
   
      break;
  }
}

void modoAnalisis() {
  if (millis() - tiempoAnterior >= intervalo) {
    tiempoAnterior = millis();
    float peso = balanza.get_units();
    Serial.println(peso);  
  }
}
