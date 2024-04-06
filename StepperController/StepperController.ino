#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>
#include "defines.h"
#include "calibration.h"
AccelStepper stepperx(1, MOTOR_X_STEP_PIN, MOTOR_X_DIR_PIN);
AccelStepper steppery(1, MOTOR_Y_STEP_PIN, MOTOR_Y_DIR_PIN);
MultiStepper steppers;
bool st_enabled = false;
void setup() {
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(END_PIN_X, INPUT_PULLUP);
  pinMode(END_PIN_Y, INPUT_PULLUP);
  stepperx.setPinsInverted(false, false, true);
  steppery.setPinsInverted(false, false, true);
  SetStepperSettings();
  stepperx.setEnablePin(ENABLE_PIN);
  steppery.setEnablePin(ENABLE_PIN);
  steppers.addStepper(stepperx);
  steppers.addStepper(steppery);
  Serial.begin(115200);
  calibrate();
}


void enable_steppers() {
  if (!st_enabled) {
    stepperx.enableOutputs();
    steppery.enableOutputs();
    st_enabled = true;
  }
}
void disable_steppers() {
  if (st_enabled) {
    stepperx.disableOutputs();
    steppery.disableOutputs();
    st_enabled = false;
  }
}
void SetStepperSettings() {
  stepperx.setMaxSpeed(MAX_SPEED);
  stepperx.setAcceleration(MAX_ACCEL);
  stepperx.setSpeed(MIN_SPEED);
  steppery.setMaxSpeed(MAX_SPEED);
  steppery.setAcceleration(MAX_ACCEL_Y);
  steppery.setSpeed(MIN_SPEED);
}
void loop() {
  int StartZeit = 0;
  if (!st_enabled) {
    enable_steppers();
  }
  if (Serial.available() > 0) {
    StartZeit = millis();
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (strcmp(command.c_str(), "MAXIMA") == 0) {
      Serial.println(String(MAX_X) + "," + String(MAX_Y));
    } else if (strcmp(command.c_str(), "POSITION") == 0) {
      Serial.println(String(stepperx.currentPosition()) + "," + String(steppery.currentPosition()));
    } else if (strcmp(command.c_str(), "CALIBRATE") == 0) {
      calibrate();
    } else if (strcmp(command.c_str(), "STATUS") == 0) {
      if (stepperx.isRunning() || steppery.isRunning())
        Serial.println("BUSY");
      else
        Serial.println("READY");
    } else {
      int delimiterIndex = command.indexOf(',');
      long movement_x = command.substring(0, delimiterIndex).toInt();   //new x pos
      long movement_y = command.substring(delimiterIndex + 1).toInt();  //new y pos
      long positions[2] = {movement_x, movement_y};
      if (movement_x >= 0 && movement_x <= MAX_X && movement_y >= 0 && movement_y <= MAX_Y) {
        SetStepperSettings();
        //steppers.moveTo(positions); For MulitStepper Libary
        //steppers.runSpeedToPosition();

        MoveToPosition(movement_x, movement_y);
        //stepperx.runToNewPosition(movement_x);
        //steppery.runToNewPosition(movement_y);
        Serial.println(millis()- StartZeit);
      }
      Serial.println("OK");
    }
  }
}

void MoveToPosition( long movement_x, long movement_y){

  stepperx.moveTo(movement_x);
  steppery.moveTo(movement_y);
  
  do{
    stepperx.run();
    steppery.run();
  }while(stepperx.isRunning() || steppery.isRunning());

  Serial.println(stepperx.currentPosition());
  Serial.println(steppery.currentPosition());

/*
  do
  {
    if(stepperx.run() || steppery.run())
    {
      continue;
    }else
    {
      Posy += increment;
      Posx += increment;
      stepperx.moveTo(Posx);
      //stepperx.run();
      Serial.println(Posx);

      steppery.moveTo(Posy);
      //steppery.run();
      Serial.println(Posy);
    }
  }while(Posx <= movement_x);
  */
}


