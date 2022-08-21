import RPi.GPIO as GPIO
import time

class UltraSonic:
    def __init__(self, TRIG, ECHO):
        self.trig = TRIG
        self.echo = ECHO
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, False)
        self.pulse_start = time.time()
        self.pulse_end = time.time()
    
    def distance(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        while GPIO.input(self.echo)==0:
            self.pulse_start = time.time()
        while GPIO.input(self.echo)==1:
            self.pulse_end = time.time()
        pulse_duration = self.pulse_end - self.pulse_start
        distance = pulse_duration * 17150
        distance = round(distance+1.15, 2)

        return distance
         
if __name__ == "__main__":
    pass