#include <L298N.h>
#include <HCSR04.h>
#include <Servo.h>
int IN2 = 2 ;
int IN1 = 4 ;
int ENA = 3;
int Tr_ULL = 5 ;
int Echo_ULL = 6 ;
int Tr_ULR = 7 ;
int Echo_ULR = 8 ;
int K1 = 5 ;
int steer ;
unsigned long cMillis = 0 ;
unsigned long pMillis = 0 ;
const long interval_1 = 0;
const long interval_2 = 0 ;
unsigned long DR = 0 ;
unsigned long DL = 0;
unsigned long error = 0 ;

UltraSonicDistanceSensor Right_Ultra(7, 8);
UltraSonicDistanceSensor Left_Ultra(5, 6);

L298N motor(ENA, IN1, IN2);
Servo myservo;

void setup() {
   delay ( 4000) ;
  myservo.attach(9);
  myservo.write(90);
  motor.setSpeed(100);
}

void loop() {
  cMillis = millis ();
  motor.forward();
  DR = (Right_Ultra.measureDistanceCm());
  DL = (Left_Ultra.measureDistanceCm()) ;
  error = DR-DL ;
  steer = K1 * error ;
  myservo.write(steer);
}
