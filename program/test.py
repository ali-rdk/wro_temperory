from ahrs import *
from time import sleep

time.sleep(1)

print('recording data')
angle = 0
while 1:
	try:
		ax, ay, az, wx, wy, wz = mpu6050_conv()
		mx, my, mz = AK8963_conv()
	except:
		continue
		
	if abs(wz+0.442) >= 0.4:
		angle += (wz + 0.442) * 0.019
	angle = round(angle)
	sleep(0.01)
