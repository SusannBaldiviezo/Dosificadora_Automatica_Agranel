#include "pantalla.h"

// Instancia de la pantalla LCD (dirección 0x27, 16 columnas x 2 filas)
LiquidCrystal_I2C lcd(0x27, 16, 2);

void inicializarPantalla() {
    lcd.init();
    lcd.backlight();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Dosificadora OK");
    lcd.setCursor(0, 1);
    lcd.print("Esperando...");
    delay(1000);
    lcd.clear();
}

void mostrarMensaje(const char* linea1, const char* linea2) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(linea1);
    lcd.setCursor(0, 1);
    lcd.print(linea2);
}

void mostrarPeso(float peso) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Peso actual:");
    lcd.setCursor(0, 1);
    lcd.print(peso, 2);
    lcd.print(" g");
}

void mostrarEstado(const char* estado) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Estado:");
    lcd.setCursor(0, 1);
    lcd.print(estado);
}

void limpiarPantalla() {
    lcd.clear();
}
