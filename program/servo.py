import RPi.GPIO as GPIO

class ServoMotor:
    def __init__(self,servo_pin ,positions = (4,7,10)):
        self.left, self.center, self.right = positions
        GPIO.setup(servo_pin, GPIO.OUT)
        self.p = GPIO.PWM(servo_pin, 50)
        self.p.start(self.center)
        self.right_error = self.right - self.center
        self.left_error = self.left - self.center
    
    def steering(self, steer):
        steer = 100 if steer > 100 else steer
        steer = -100 if steer < -100 else steer
        correction = steer / 100
        if correction >= 0:
            data = (self.right_error * correction) + self.center
        else:
            data = (self.left_error * -correction) + self.center
        self.p.ChangeDutyCycle(data)
        #print(data)

if __name__ == "__main__":
    pass