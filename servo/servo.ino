#include <Servo.h>
int servo = 3;
Servo servo_1;
void setup() {
  // put your setup code here, to run once:
servo_1.attach(servo);
}

void loop() {
  // put your main code here, to run repeatedly:
servo_1.write(60);
delay(1000);
//servo_1.write(90);
//delay(1000);
//servo_1.write(60);
//delay(1000);
//servo_1.write(30);
//delay(1000);


}
