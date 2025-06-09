#ifndef BOTONES_H
#define BOTONES_H

#include <Arduino.h>


#define BTN_INCREMENTAR_PIN 2
#define BTN_DECREMENTAR_PIN 3
#define BTN_CONFIRMAR_PIN   4

// Estados de los botones
typedef enum {
    BTN_IDLE,
    BTN_PRESSED,
    BTN_HELD,
    BTN_RELEASED
} EstadoBoton;

// Estructura para cada botón
typedef struct {
    uint8_t pin;
    bool estadoActual;
    bool estadoAnterior;
    unsigned long tiempoUltimoCambio;
    unsigned long debounceDelay;
    EstadoBoton estado;
} Boton;


void inicializarBotones(Boton* b1, Boton* b2, Boton* b3);


void actualizarBoton(Boton* boton);

#endif
