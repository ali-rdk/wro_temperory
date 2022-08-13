int motor1 = 5;
int motor2 = 6;
void setup() {
  // put your setup code here, to run once:
  pinMode(motor1, OUTPUT);
    pinMode(motor2, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(motor1, 0);
  analogWrite(motor2, 200);

}
