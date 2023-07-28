#include <Servo.h>
#include <Wire.h>
#include "SparkFun_VCNL4040_Arduino_Library.h"

const int actuator1Pin = 9;   // PWM pin for actuator 1
const int actuator2Pin = 10;  // PWM pin for actuator 2
const int controlPin1 = 4;    // Control pin 1 for DC motor
const int controlPin2 = 5;    // Control pin 2 for DC motor

int minActuatorValue = 1000;
int maxActuatorValue = 2000;
int minMappedValue1 = -300;  // Corresponding to the values the xbox controller sends from Python
int maxMappedValue1 = -100;  // Corresponding to the values the xbox controller sends from Python
int minMappedValue2 = -600;
int maxMappedValue2 = -800;

const int initialPosition1 = -200;    // Initial position to reset the actuators to mid-point
const int initialPosition2 = -700;  // Initial position to reset the actuators to mid-point

Servo actuator1;
Servo actuator2;
VCNL4040 proximitySensor;

long startingProxValue = 0;
long deltaNeeded = 0;
boolean nothingThere = false;

void setup() {
  pinMode(controlPin1, OUTPUT);
  pinMode(controlPin2, OUTPUT);

  actuator1.attach(actuator1Pin);
  actuator2.attach(actuator2Pin);

  Serial.begin(115200);  // Set the baud rate to match the Python code

  Wire.begin(); //Join i2c bus

  while (proximitySensor.begin() == false)
  {
    Serial.println("Device not found. Please check wiring.");
    //while (1); //Freeze!
  }

}

bool ignoreData = false; // Explicit initialization

void loop() {
  
   if (!ignoreData && Serial.available() > 0) {
    int receivedNumber = Serial.parseInt();
    Serial.println(receivedNumber);
    //int proxValue = proximitySensor.getProximity();
    
    if (receivedNumber == 0) {
      Serial.println("Zero");
    }
    else if (receivedNumber == 1000) {
      digitalWrite(controlPin1, LOW);
      digitalWrite(controlPin2, HIGH);
    }
    else if (receivedNumber == 2000) {
      digitalWrite(controlPin1, LOW);
      digitalWrite(controlPin2, LOW);
    }
    else if (receivedNumber < -400) {
      moveActuator2(receivedNumber);
    }
    else if (receivedNumber > -350) {
      moveActuator1(receivedNumber);
    }
  }
  //Get proximity value. The value ranges from 0 to 65535
  //so we need an unsigned integer or a long.
    unsigned int proxValue = proximitySensor.getProximity(); 
    delay(10);
    Serial.println(proxValue);
  if ((proxValue > 3500) && (proxValue < 30000)){
    ignoreData = true;
    delay(1000);
    actuator1.writeMicroseconds(1750);
    actuator2.writeMicroseconds(1750);
    digitalWrite(controlPin1, LOW);
    digitalWrite(controlPin2, HIGH);
    delay(24000);
    digitalWrite(controlPin1, LOW);
    digitalWrite(controlPin2, LOW);
    actuator1.writeMicroseconds(1500);
    actuator2.writeMicroseconds(1500);
    ignoreData = false;
  }
}

void moveActuator1(int position) {
  int mappedValue = map(position, minMappedValue1, maxMappedValue1, minActuatorValue, maxActuatorValue);
  actuator1.writeMicroseconds(mappedValue);
}

void moveActuator2(int position) {
  int mappedValue = map(position, minMappedValue2, maxMappedValue2, minActuatorValue, maxActuatorValue);
  actuator2.writeMicroseconds(mappedValue);
}
