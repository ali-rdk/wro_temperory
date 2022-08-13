int ultra_trig = 12;
int ultra_r = 8;
int ultra_c = 9;
int ultra_l = 10;
long duration; // variable for the duration of sound wave travel
int distance_r;
int distance_c;
int distance_l;
void setup() {
  // put your setup code here, to run once:
  pinMode(ultra_trig, OUTPUT);
  pinMode(ultra_r, INPUT);
  pinMode(ultra_c, INPUT);
  pinMode(ultra_l, INPUT);
  Serial.begin(9600); 

}

void loop() {
  // put your main code here, to run repeatedly:
digitalWrite(ultra_trig, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(ultra_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(ultra_trig, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(ultra_r, HIGH);
  // Calculating the distance
  distance_r = duration * 0.034 / 2;
    if (distance_r <=duration * 0.034 / 2){
  distance_r = duration * 0.034 / 2;}
  delay(100);
  digitalWrite(ultra_trig, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(ultra_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(ultra_trig, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(ultra_c, HIGH);
  // Calculating the distance
  distance_c = duration * 0.034 / 2;
    if (distance_c <=duration * 0.034 / 2){
  distance_c = duration * 0.034 / 2;}
  delay(100);
  digitalWrite(ultra_trig, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(ultra_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(ultra_trig, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(ultra_l, HIGH);
  // Calculating the distance
  if (distance_l <=duration * 0.034 / 2){
  distance_l = duration * 0.034 / 2;}

  delay(100);
  Serial.print("left = ");
  Serial.println(distance_l);

   Serial.print("center = ");
  Serial.println(distance_c);

    Serial.print("right = ");
  Serial.println(distance_r);

  
}
