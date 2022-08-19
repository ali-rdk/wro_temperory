import RPi.GPIO as GPIO

class MainMotor:
    def __init__(self, motor1_pin, motor2_pin):
        GPIO.setup(motor1_pin, GPIO.OUT)
        GPIO.setup(motor2_pin, GPIO.OUT)
        self.motor = GPIO.PWM(motor2_pin, 1000)
        self.motor.start(0)
        GPIO.output(motor1_pin, GPIO.LOW)
    
    def speed(self, power):
            self.motor.ChangeDutyCycle(power)

# Forward=12
# Backward=26
if __name__ == "__main__":
    pass











