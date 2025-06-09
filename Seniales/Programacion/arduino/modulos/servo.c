#include "servo.h"

Servo compuerta;

void inicializarServo() {
    compuerta.attach(SERVO_PIN);
    cerrarCompuerta();  
}

void abrirCompuerta() {
    compuerta.write(180); 
}

void cerrarCompuerta() {
    compuerta.write(150);  
}
