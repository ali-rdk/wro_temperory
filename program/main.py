import RPi.GPIO as GPIO
from ultrasonics import UltraSonic
from servo import ServoMotor
from motor import MainMotor
from gyro import Gyro
from pid import Pid
import time
from numpy import mean
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

ultra_l = UltraSonic(6, 5)
ultra_c = UltraSonic(24, 23)
ultra_r = UltraSonic(22, 27)

servo = ServoMotor(13, positions=[4, 7, 10])

motor = MainMotor(12, 26)

gyro = Gyro()

pid = Pid(5, 0, 0)
forward_d = []
for i in range(3):
    forward_d.append(ultra_c.distance())
print(mean(forward_d))
a = 0
side = 0
flag = True
target = 0
t = time.time() - 2
t1 = time.time()
wall_target_correction = 0
motor.speed(45)
while True:
    while True:
        b = round(gyro.angle(), 2) + wall_target_correction
        print(b, target, a)
        if time.time() - t1 >= 2:
            wall_target_correction = -40 / ultra_r.distance()
            wall_target_correction = 40 / ultra_l.distance()
            t1 = time.time()
        a = pid.pid(b, target)
        #print(b - target)
        servo.steering(a)
        forward_d.pop(0)
        forward_d.append(ultra_c.distance())
        #if abs(a) <= 5 and not flag:
            #gyro.reset()
            #target = 0
            #flag = True
        if time.time() - t >= 4 and mean(forward_d) <= 60:
            break
    if side == 0:
        right_d = 0
        for i in range(3):
            right_d += ultra_r.distance()
        right_d /= 3
        side = -1 if right_d >= 5 and right_d <= 200 else 1
    target += 90 * side
    t = time.time()
    flag = False


