from ahrs import *

time.sleep(1)

print('recording data')

while 1:
	try:
		ax, ay, az, wx, wy, wz = mpu6050_conv()
		mx, my, mz = AK8963_conv()
	except:
		continue
		
	print('{}'.format('-'*30))
	print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z {2:2.2f}= '.format(ax,ay,az))
	print('gyro [dps]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
	print('mag [uT]:   x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(mx,my,mz))
	print('{}'.format('-'*30))
	time.sleep(1)
