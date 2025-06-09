#ifndef BUZZER_H
#define BUZZER_H

#include <Arduino.h>

#define BUZZER_PIN 7

void inicializarBuzzer();
void sonarBuzzer(int tiempo);

#endif