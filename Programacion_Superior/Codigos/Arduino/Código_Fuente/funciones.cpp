#include "Dispensador.h"  // Archivo de cabecera con constantes y definiciones

// Objetos
HX711 scale;                      // Sensor de peso
LiquidCrystal_I2C lcd(0x27, 16, 2); // Pantalla LCD I2C 16x2
Servo servo;                      // Servo motor para dispensar

// Variables globales del sistema
EstadoSistema estadoActual = CONFIGURACION;  
int peso_umbral = 100;            
bool sistema_activo = false;      
unsigned long ultimo_envio = 0;   
float ultimo_peso_dispensado = 0.0;

// Inicializa componentes (pantalla, sensor, pines, servo)
void inicializarSistema() {
  lcd.init();
  lcd.backlight();
  scale.begin(DOUT, CLK);
  scale.set_scale(FACTOR_CALIBRACION);
  scale.tare();  // Realiza tara al inicio

  pinMode(BTN_UP, INPUT_PULLUP);
  pinMode(BTN_DOWN, INPUT_PULLUP);
  pinMode(BTN_START, INPUT_PULLUP);

  servo.attach(SERVO_PIN);
  servo.write(SERVO_CERRADO);  // Servo cerrado por defecto

  pinMode(BUZZER_LED_PIN, OUTPUT);
  digitalWrite(BUZZER_LED_PIN, LOW);

  mostrarMensaje("Sistema Listo", "Peso: 0.0g");
}

// Retorna el peso leído
float leerPeso() {
  return scale.get_units(3);
}

// Muestra información en pantalla: peso actual, meta y último peso servido
void actualizarPantalla(float peso) {
  lcd.setCursor(0, 0);
  lcd.print("Peso: ");
  lcd.print(peso, 1);
  lcd.print("g  ");

  lcd.setCursor(13, 0);
  lcd.print("Ult");

  lcd.setCursor(0, 1);
  lcd.print("Meta: ");
  lcd.print(peso_umbral);
  lcd.print("g ");

  lcd.setCursor(11, 1);
  lcd.print(ultimo_peso_dispensado, 1);
  lcd.print("g");
}

// Muestra un mensaje personalizado en la pantalla del LCD
void mostrarMensaje(String linea1, String linea2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(linea1);
  lcd.setCursor(0, 1);
  lcd.print(linea2);
}

// Maneja los botones físicos UP, DOWN y START
void manejarBotones() {
  if (digitalRead(BTN_UP) == LOW) {
    peso_umbral = min(peso_umbral + PASO_UMBRAL, UMBRAL_MAX);
    Serial.print("UMBRAL:");
    Serial.println(peso_umbral);
    actualizarPantalla(leerPeso());
    delay(300);
  }

  if (digitalRead(BTN_DOWN) == LOW) {
    peso_umbral = max(peso_umbral - PASO_UMBRAL, UMBRAL_MIN);
    Serial.print("UMBRAL:");
    Serial.println(peso_umbral);
    actualizarPantalla(leerPeso());
    delay(300);
  }

  detectarBotonStart();
}

// Detecta si el botón START fue presionado brevemente o mantenido para hacer tara
void detectarBotonStart() {
  static unsigned long tiempoInicio = 0;
  static bool esperandoLiberacion = false;

  if (digitalRead(BTN_START) == LOW) {
    if (!esperandoLiberacion) {
      tiempoInicio = millis();
      esperandoLiberacion = true;
    } else if (millis() - tiempoInicio >= 2000) {
      // Si se mantiene presionado por más de 2 segundos hace tara
      scale.tare();
      mostrarMensaje("Tara realizada", "Peso: 0.0g");
      Serial.println("TARA MANUAL EJECUTADA");
      delay(1000);
      esperandoLiberacion = false;
    }
  } else {
    // Si se soltó antes de 2 segundos iniciar dispensado
    if (esperandoLiberacion && millis() - tiempoInicio < 2000) {
      if (!sistema_activo) {
        sistema_activo = true;
        estadoActual = ACTIVAR_MOTOR;
      }
    }
    esperandoLiberacion = false;
  }
}

// Genera un beep simple de inicio
void beepInicio() {
  tone(BUZZER_LED_PIN, 1000, 200);
}

// Genera tres beeps para indicar que el proceso ha finalizado
void beepFin() {
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_LED_PIN, 1200, 150);
    delay(300);
  }
}

// Abre el servo (inicia el flujo del producto)
void abrirServo() {
  servo.write(SERVO_ABIERTO);
}

// Cierra el servo (detiene el flujo del producto)
void cerrarServo() {
  servo.write(SERVO_CERRADO);
}

// Finaliza el proceso de dispensado
void finalizarDispensado() {
  float peso_final = leerPeso();
  Serial.print("FINAL:");
  Serial.println(peso_final, 1);

  beepFin();  
  mostrarMensaje("Servido completo", "Peso: " + String(peso_final, 1) + "g");
  delay(7000);  // Espera para que el usuario vea el resultado y retire el peso
  scale.tare(); // Prepara para una nueva medición

  ultimo_peso_dispensado = peso_final;
  sistema_activo = false;
  estadoActual = CONFIGURACION;
}

// Interpreta comandos enviados por el puerto serial (desde PC o servidor)
void leerComandosSerial() {
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim(); 

    if (comando.startsWith("SET:")) {
      // Comando SET: ajusta el peso objetivo
      int nuevo_umbral = comando.substring(4).toInt();
      if (nuevo_umbral >= UMBRAL_MIN && nuevo_umbral <= UMBRAL_MAX) {
        peso_umbral = nuevo_umbral;
        lcd.setCursor(0, 1);
        lcd.print("Meta: ");
        lcd.print(peso_umbral);
        lcd.print("g  ");
      }
    } else if (comando == "START") {
      // Comando para iniciar el sistema
      if (!sistema_activo) {
        sistema_activo = true;
        estadoActual = ACTIVAR_MOTOR;
      }
    } else if (comando == "TARE") {
      // Comando para hacer tara
      scale.tare();
      Serial.println("TARA:OK");
    }
  }
}

// Envía el peso actual por serial cada cierto tiempo
void enviarPorSerialPeriodicamente(float peso) {
  if (millis() - ultimo_envio >= INTERVALO_ENVIO) {
    Serial.print("PESO:");
    Serial.println(peso, 1);
    ultimo_envio = millis();
  }
}
