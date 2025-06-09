#ifndef PANTALLA_H
#define PANTALLA_H

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

// Debemos cambiar la dirección si es necesario
extern LiquidCrystal_I2C lcd;


void inicializarPantalla();


void mostrarMensaje(const char* linea1, const char* linea2);

void mostrarPeso(float peso);


void mostrarEstado(const char* estado);


void limpiarPantalla();

#endif
