#include "buzzer.h"

void inicializarBuzzer() {
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);
}

void sonarBuzzer(int tiempo) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(tiempo);
    digitalWrite(BUZZER_PIN, LOW);
}
