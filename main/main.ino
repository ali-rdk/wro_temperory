#include <Servo.h>
#include <HCSR04.h>
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
UltraSonicDistanceSensor ultra_r(12, 8);
UltraSonicDistanceSensor ultra_c(12, 9); 
UltraSonicDistanceSensor ultra_l(12, 10);  
Servo servo_1;
int servo = 3;
float error;
float correction;
float straught_distance;
float right_distance;
int motor1 = 5;
int motor2 = 6;
int state = 0;
int side = 0;
long timer = 0;
long t = 0;
int servo_position;
int target_angle = 0;
int middle_servo = 60;
void setup() {
    pinMode(motor1, OUTPUT);
    pinMode(motor2, OUTPUT);
    Serial.begin(9600); 
    servo_1.attach(servo);
    Wire.begin();
    servo_1.write(middle_servo);
    Serial.println("calibrate servo");
    delay(10000);
    byte status = mpu.begin();
    Serial.print(F("MPU6050 status: "));
    Serial.println(status);
    while(status!=0){ } // stop everything if could not connect to MPU6050
    Serial.println(F("Calculating offsets, do not move MPU6050"));
    delay(1000);
    mpu.calcOffsets(true,true); // gyro and accelero
    Serial.println("Done!\n");

}

void loop() {
  analogWrite(motor1, 0);
  analogWrite(motor2, 150);
  mpu.update();
  if (state == 0){
    straught_distance = 0;
    for (int i=0; i != 3; i++){straught_distance = straught_distance + ultra_c.measureDistanceCm();}
    straught_distance = straught_distance/3;
    while(straught_distance >= 70 || straught_distance <= 3){
      straught_distance = 0;
      for (int i=0; i != 3; i++){straught_distance = straught_distance + ultra_c.measureDistanceCm();}
      straught_distance = straught_distance/3;
      Serial.print("in loop");
      mpu.update();
      error = mpu.getAngleZ()- target_angle;
      correction = middle_servo - (error*2);
      if (correction >= 90){correction = 90;}
      if (correction <= 35){correction = 35;}
      servo_1.write(correction);
      }
    right_distance = 0;
    for (int i=0; i != 3; i++){right_distance = right_distance + ultra_r.measureDistanceCm();}
    right_distance = right_distance/3;
    if (right_distance <= 120 && right_distance >= 5 && ultra_r.measureDistanceCm() <= 120 && ultra_r.measureDistanceCm()>=5){side = 1;}
    else{side = 1;}
    state = 1;
    }

  Serial.println(target_angle);
  error = mpu.getAngleZ()- target_angle;
  correction = middle_servo - (error*2);
  if (correction >= 100){correction = 100;}
  if (correction <= 20){correction = 20;}
  if (abs(error*2)>=20){    analogWrite(motor1, 0);analogWrite(motor2, 170);}
  else{    analogWrite(motor1, 0);analogWrite(motor2, 150);}
  servo_1.write(correction);
  straught_distance = 0;
  for (int i=0; i != 3; i++){straught_distance = straught_distance + ultra_c.measureDistanceCm();}
  straught_distance = straught_distance/3;
  if (straught_distance <= 70 && straught_distance >= 5 && ultra_c.measureDistanceCm()<=70&&ultra_c.measureDistanceCm()>=5 && millis()-timer >=3000 &&abs(mpu.getAngleZ()- target_angle)<=5  ){
    if (side == 1){target_angle = target_angle - 90;Serial.println("right");}
    else if (side == -1){target_angle = target_angle + 90;Serial.println("left");}
    timer = millis();
  }
  
  
}






  
