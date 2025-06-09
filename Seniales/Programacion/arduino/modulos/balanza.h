#ifndef BALANZA_H
#define BALANZA_H

#include <Arduino.h>
#include "HX711.h"


#define DOUT  A1
#define SCK   A0


void inicializarBalanza();
float leerPeso();           
void taraBalanza();         

#endif
