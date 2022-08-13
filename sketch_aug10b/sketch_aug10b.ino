int servo = 5;
void setup() {
  // put your setup code here, to run once:
servo_1.attach(servo);
}

void loop() {
  // put your main code here, to run repeatedly:
servo_1.write(90);
}
