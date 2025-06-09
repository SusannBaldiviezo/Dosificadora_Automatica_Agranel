#include "balanza.h"


HX711 balanza;

void inicializarBalanza() {
    balanza.begin(DOUT, SCK);
    Serial.println("Inicializando balanza...");
    delay(1000);

    
    while (!balanza.is_ready()) {
        Serial.println("Esperando HX711...");
        delay(500);
    }

   
    balanza.set_scale(432.802093); 
    balanza.tare();             
    Serial.println("Balanza lista.");
}

float leerPeso() {
    return balanza.get_units(5); 
}

void taraBalanza() {
    balanza.tare();
}
