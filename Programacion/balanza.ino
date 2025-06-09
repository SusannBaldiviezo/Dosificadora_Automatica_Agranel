#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "HX711.h"
#include <Servo.h>

// Configuración de pines
#define DOUT 2
#define CLK 3
#define BTN_UP 4
#define BTN_DOWN 5
#define BTN_START 6
#define SERVO_PIN 9
#define BUZZER_LED_PIN 10

// Configuración del sistema
const float FACTOR_CALIBRACION = 410.260009;
const int PASO_UMBRAL = 50;
const int UMBRAL_MIN = 100;
const int UMBRAL_MAX = 5000;
const int SERVO_CERRADO = 180;
const int SERVO_ABIERTO = 150;

// Objetos globales
HX711 scale;
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo servo;

// Variables de estado
int peso_umbral = UMBRAL_MIN;
unsigned long ultima_transmision = 0;
const unsigned long INTERVALO_TRANSMISION = 500; // ms

void setup() {
  Serial.begin(9600);
  
  // Inicialización LCD
  lcd.init();
  lcd.backlight();
  mostrarMensajeInicial();
  
  // Inicialización balanza
  scale.begin(DOUT, CLK);
  scale.set_scale(FACTOR_CALIBRACION);
  scale.tare();
  
  // Configuración de pines
  pinMode(BTN_UP, INPUT_PULLUP);
  pinMode(BTN_DOWN, INPUT_PULLUP);
  pinMode(BTN_START, INPUT_PULLUP);
  pinMode(BUZZER_LED_PIN, OUTPUT);
  
  // Inicialización servo
  servo.attach(SERVO_PIN);
  servo.write(SERVO_CERRADO);
  
  Serial.println("Sistema iniciado");
}

void loop() {
  // Manejo de comandos seriales
  manejarComandosSeriales();
  
  // Lectura y procesamiento del peso
  float peso_actual = scale.get_units(3);
  
  // Actualización de la pantalla
  actualizarPantalla(peso_actual);
  
  // Transmisión periódica del peso
  if (millis() - ultima_transmision >= INTERVALO_TRANSMISION) {
    transmitirPeso(peso_actual);
    ultima_transmision = millis();
  }
  
  // Manejo de botones
  manejarBotones();
  
  // Pequeña pausa para estabilidad
  delay(50);
}

// Funciones auxiliares
void mostrarMensajeInicial() {
  lcd.setCursor(0, 0);
  lcd.print("Iniciando sistema");
  lcd.setCursor(0, 1);
  lcd.print("Espere por favor...");
  delay(1500);
  lcd.clear();
}

void manejarComandosSeriales() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    if (comando.startsWith("SET:")) {
      int nuevo_umbral = comando.substring(4).toInt();
      if (nuevo_umbral >= UMBRAL_MIN && nuevo_umbral <= UMBRAL_MAX) {
        peso_umbral = nuevo_umbral;
        Serial.print("Umbral actualizado:");
        Serial.println(peso_umbral);
      }
    } 
    else if (comando == "START") {
      iniciarProcesoServido();
    }
  }
}

void transmitirPeso(float peso) {
  // Formato estructurado para fácil parseo
  Serial.print("PESO:");
  Serial.println(peso, 1);
}

void actualizarPantalla(float peso) {
  lcd.setCursor(0, 0);
  lcd.print("Peso: ");
  lcd.print(peso, 1);
  lcd.print("g   ");
  
  lcd.setCursor(0, 1);
  lcd.print("Meta: ");
  lcd.print(peso_umbral);
  lcd.print("g   ");
}

void manejarBotones() {
  // Botón UP
  if (digitalRead(BTN_UP) == LOW) {
    peso_umbral = min(peso_umbral + PASO_UMBRAL, UMBRAL_MAX);
    Serial.print("Umbral aumentado:");
    Serial.println(peso_umbral);
    delay(300); // Debounce
  }
  
  // Botón DOWN
  if (digitalRead(BTN_DOWN) == LOW) {
    peso_umbral = max(peso_umbral - PASO_UMBRAL, UMBRAL_MIN);
    Serial.print("Umbral disminuido:");
    Serial.println(peso_umbral);
    delay(300); // Debounce
  }
  
  // Botón START
  if (digitalRead(BTN_START) == LOW) {
    iniciarProcesoServido();
  }
}

void iniciarProcesoServido() {
  Serial.println("INICIANDO_PROCESO");
  float peso_actual = scale.get_units(5);
  
  // Señal acústica de inicio
  tone(BUZZER_LED_PIN, 1000, 200);
  delay(400);
  tone(BUZZER_LED_PIN, 1000, 200);
  
  // Abrir servo gradualmente
  for (int ang = SERVO_CERRADO; ang >= SERVO_ABIERTO; ang--) {
    servo.write(ang);
    delay(90);
  }
  
  // Esperar hasta alcanzar el peso deseado
  while (scale.get_units(3) < peso_umbral - 10) {
    peso_actual = scale.get_units(3);
    transmitirPeso(peso_actual);
    delay(200);
  }
  
  // Cerrar servo
  servo.write(SERVO_CERRADO);
  
  // Señal acústica de finalización
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_LED_PIN, 1200, 150);
    delay(300);
  }
  
  Serial.println("PROCESO_COMPLETADO");
  Serial.print("PESO_FINAL:");
  Serial.println(peso_actual, 1);
}
