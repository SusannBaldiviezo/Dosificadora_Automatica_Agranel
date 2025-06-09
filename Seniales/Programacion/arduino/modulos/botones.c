#include "botones.h"

void inicializarBotones(Boton* b1, Boton* b2, Boton* b3) {
    b1->pin = BTN_INCREMENTAR_PIN;
    b2->pin = BTN_DECREMENTAR_PIN;
    b3->pin = BTN_CONFIRMAR_PIN;

    Boton* botones[3] = {b1, b2, b3};

    for (int i = 0; i < 3; i++) {
        pinMode(botones[i]->pin, INPUT_PULLUP);
        botones[i]->estadoActual = digitalRead(botones[i]->pin);
        botones[i]->estadoAnterior = botones[i]->estadoActual;
        botones[i]->tiempoUltimoCambio = 0;
        botones[i]->debounceDelay = 50; //  ms
        botones[i]->estado = BTN_IDLE;
    }
}

void actualizarBoton(Boton* boton) {
    bool lectura = digitalRead(boton->pin);

    if (lectura != boton->estadoAnterior) {
        boton->tiempoUltimoCambio = millis();
    }

    if ((millis() - boton->tiempoUltimoCambio) > boton->debounceDelay) {
        if (lectura != boton->estadoActual) {
            boton->estadoActual = lectura;
            if (lectura == LOW) {
                boton->estado = BTN_PRESSED;
            } else {
                boton->estado = BTN_RELEASED;
            }
        } else {
            boton->estado = BTN_IDLE;
        }
    }

    boton->estadoAnterior = lectura;
}
