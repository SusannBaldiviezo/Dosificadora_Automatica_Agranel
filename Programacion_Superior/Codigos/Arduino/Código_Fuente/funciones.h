#ifndef DISPENSADOR_H
#define DISPENSADOR_H

// Librerías necesarias para los periféricos
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>  // Pantalla LCD I2C
#include "HX711.h"              // Celda de carga
#include <Servo.h>              // Servo motor

//MACROS

// Pines utilizados
#define DOUT 2                 
#define CLK 3                  
#define BTN_UP 4               
#define BTN_DOWN 5             
#define BTN_START 6            
#define SERVO_PIN 9            
#define BUZZER_LED_PIN 10      

// Constantes del sistema
#define FACTOR_CALIBRACION 410.459991  
#define PASO_UMBRAL 50                 
#define UMBRAL_MIN 100                 
#define UMBRAL_MAX 5000                
#define SERVO_CERRADO 180              
#define SERVO_ABIERTO 100              
#define INTERVALO_ENVIO 500            

// Máquina de estados del dispensador
enum EstadoSistema {
  CONFIGURACION,       // Estado inicial, espera configuración
  ACTIVAR_MOTOR,       // Abre el servo para comenzar a dispensar
  CONTROL_CANTIDAD,    // Controla el peso durante el dispensado
  FINALIZACION         // Finaliza el proceso, cierra servo, resetea
};

// Declaración de variables globales compartidas
extern EstadoSistema estadoActual;           
extern int peso_umbral;                      
extern bool sistema_activo;                  
extern unsigned long ultimo_envio;           
extern float ultimo_peso_dispensado;         

// Funciones para el funcionamiento del proyecto
void inicializarSistema();                           
float leerPeso();                                    
void manejarBotones();                               
void detectarBotonStart();                           
void actualizarPantalla(float peso);                 
void mostrarMensaje(String linea1, String linea2);   
void leerComandosSerial();                           
void beepInicio();                                   
void beepFin();                                      
void abrirServo();                                   
void cerrarServo();                                  
void finalizarDispensado();                          
void enviarPorSerialPeriodicamente(float peso);      

#endif
