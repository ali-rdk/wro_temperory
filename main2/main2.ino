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
int motor1 = 10;
int motor2 = 11;

int middle_servo = 90;

float wall_c = 0;
int state = 0;
int side = 0;
long timer = 0;
int target_angle = 0;
float sum_error = 0;
float error;
float d = 0;
float last_error = 0;
float correction;
int servo_position;
float start_c,start_r,start_l;
float straught_distance,c,r,l;
float right_distance;
boolean flag = true;

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
    pinMode(8, INPUT);
    pinMode(12, OUTPUT);
    while (digitalRead(8) == LOW){digitalWrite(12,HIGH);}digitalWrite(12,LOW);
    for (int i=0; i != 3; i++){start_c = start_c + ultra_c.measureDistanceCm();}
        start_c = start_c/3;
    for (int i=0; i != 3; i++){start_r = start_r + ultra_r.measureDistanceCm();}
        start_c = start_c/3;
    for (int i=0; i != 3; i++){start_l = start_l + ultra_l.measureDistanceCm();}
        start_l = start_l/3;
    target_angle = mpu.getAngleZ();

}

void loop() {
  analogWrite(motor1, 0);
  analogWrite(motor2, 100);
  mpu.update();
  if (flag == true){
  target_angle = mpu.getAngleZ();flag = false;}
//  Serial.print(target_angle);
  Serial.println(mpu.getAngleZ());
  
  
  error = mpu.getAngleZ()- target_angle;
  sum_error += error;
  d = error - last_error;
  last_error = error;
  correction = middle_servo + (error*2)+(d*1);
  correction +=  wall_c;
  if (correction >= 160){correction = 160;}
  if (correction <= 20){correction = 20;}
  servo_1.write(correction );
  straught_distance = 0;
  
  for (int i=0; i != 3; i++){straught_distance = straught_distance + ultra_c.measureDistanceCm();}
  straught_distance = straught_distance/3;

  c = ultra_c.measureDistanceCm();
  r = ultra_r.measureDistanceCm();
  l = ultra_l.measureDistanceCm();
  if (target_angle == 360 * 3 && start_c >= c){
    analogWrite(motor1, 0);
  analogWrite(motor2, 0);
  while(1){continue;}}
  if (r <= 30 && r >= 5){wall_c = -130/r;}
  else if (l <= 30 && l >= 5){wall_c = 130/l;}
  else{wall_c = 0;}
  if (straught_distance <= 50 && straught_distance >= 5 && c<=50 && c>=5 && millis()-timer >=3000 &&abs(mpu.getAngleZ()- target_angle)<=10  ){
    if (state == 0){
      right_distance = 0;
      for (int i=0; i != 3; i++){right_distance = right_distance + r;}
        right_distance = right_distance/3;
      if (right_distance <= 120 && right_distance >= 5 && r <= 120 && r>=5){side = -1;}
      else{side = -1;}
      state = 1;
    }
    if (side == 1){target_angle = target_angle - 90;Serial.println("right");}
    else if (side == -1){target_angle = target_angle + 90;Serial.println("left");}
    timer = millis();
  }
  
  
}
