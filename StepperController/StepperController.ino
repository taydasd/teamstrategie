#include <Arduino.h>
#include <AccelStepper.h>
#define ENABLE_PIN 8
#define MOTOR_Y_STEP_PIN 2
#define MOTOR_Y_DIR_PIN 5
#define MOTOR_X_STEP_PIN 3
#define MOTOR_X_DIR_PIN 6
#define END_PIN_X 9
#define END_PIN_Y 10
#define MAX_ACCEL 3000
#define MAX_SPEED 4000
AccelStepper stepperx(1, MOTOR_X_STEP_PIN, MOTOR_X_DIR_PIN);
AccelStepper steppery(1, MOTOR_Y_STEP_PIN, MOTOR_Y_DIR_PIN);
void setup() {
  stepperx.setPinsInverted(false, false, true);
  steppery.setPinsInverted(false, false, true);
  stepperx.setMaxSpeed(MAX_SPEED);
  stepperx.setAcceleration(MAX_ACCEL);
  stepperx.setSpeed(MAX_SPEED);
  steppery.setMaxSpeed(MAX_SPEED);
  steppery.setAcceleration(MAX_ACCEL);
  steppery.setSpeed(MAX_SPEED);
  stepperx.setEnablePin(ENABLE_PIN);
  steppery.setEnablePin(ENABLE_PIN);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0)
    {
        String command = Serial.readStringUntil('\n');
    }
}
