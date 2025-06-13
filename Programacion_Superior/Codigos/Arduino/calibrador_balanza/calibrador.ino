#include "HX711.h"

#define DOUT  2
#define CLK   3

HX711 scale;

void setup() {
  Serial.begin(9600);
  scale.begin(DOUT, CLK);

  Serial.println("<<< CALIBRACIÓN DE BALANZA >>>");
  Serial.println("Asegúrate de que no haya peso sobre la celda.");
  delay(3000);
  
  scale.set_scale(); // Sin factor inicial
  scale.tare();      // Pone en cero

  Serial.println("Balanza puesta a cero.");
  Serial.println("\nColoca un peso conocido (ej. 500g), luego escribe el valor en gramos y presiona ENTER:");
}

void loop() {
  if (Serial.available() > 0) {
    float peso_real = Serial.readStringUntil('\n').toFloat();  // Leer entrada como número decimal
    Serial.print("Peso introducido: ");
    Serial.print(peso_real);
    Serial.println(" g");

    Serial.println("Leyendo valor del sensor...");
    delay(2000); 

    long lectura = scale.get_units(10); // Promedia 10 lecturas
    Serial.print("Valor leído del sensor: ");
    Serial.println(lectura);

    if (peso_real > 0) {
      float factor_calibracion = lectura / peso_real;
      Serial.print("\n✅ Tu factor de calibración es: ");
      Serial.println(factor_calibracion, 6);
      Serial.println("\n👉 Usa este valor en tu código con: scale.set_scale(factor_calibracion);");
    } else {
      Serial.println("⚠ El valor ingresado no es válido.");
    }

    while (true); 
  }
}