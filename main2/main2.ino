#include <Servo.h>
#include <HCSR04.h>
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
UltraSonicDistanceSensor ultra_r(4, 5);
UltraSonicDistanceSensor ultra_c(3, 2); 
UltraSonicDistanceSensor ultra_l(6, 7);  
Servo servo_1;
int servo = 9;
float error;
float correction;
float straught_distance;
float right_distance;
int motor1 = 10;
int motor2 = 11;
int state = 0;
int side = 0;
long timer = 0;
int servo_position;
int target_angle = 0;
int middle_servo = 90;

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
    for (int i=0; i != 3; i++){right_distance = right_distance + ultra_r.measureDistanceCm();}
        right_distance = right_distance/3;

}

void loop() {
  analogWrite(motor1, 0);
  analogWrite(motor2, 150);
  mpu.update();
  
  Serial.print(target_angle);
  Serial.println(mpu.getAngleZ());


  error = mpu.getAngleZ()- target_angle;
  correction = middle_servo + (error*1);
  if (correction >= 100){correction = 100;}
  if (correction <= 20){correction = 20;}
  servo_1.write(correction);
  straught_distance = 0;
  for (int i=0; i != 3; i++){straught_distance = straught_distance + ultra_c.measureDistanceCm();}
  straught_distance = straught_distance/3;
  if (straught_distance <= 70 && straught_distance >= 5 && ultra_c.measureDistanceCm()<=70&&ultra_c.measureDistanceCm()>=5 && millis()-timer >=3000 &&abs(mpu.getAngleZ()- target_angle)<=5  ){
    if (state == 0){
      right_distance = 0;
      for (int i=0; i != 3; i++){right_distance = right_distance + ultra_r.measureDistanceCm();}
        right_distance = right_distance/3;
      if (right_distance <= 120 && right_distance >= 5 && ultra_r.measureDistanceCm() <= 120 && ultra_r.measureDistanceCm()>=5){side = -1;}
      else{side = -1;}
      state = 1;
    }
    if (side == 1){target_angle = target_angle - 90;Serial.println("right");}
    else if (side == -1){target_angle = target_angle + 90;Serial.println("left");}
    timer = millis();
  }
  
  
}
