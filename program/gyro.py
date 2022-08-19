from ahrs import *
import time
# right is negetive
class Gyro:
    def __init__(self):
        self.temp_angle = 0
        self.perma_angle = 0
        self.last_read_time = time.time()
    def angle(self):

        try:
            ax,ay,az,wx,wy,wz = mpu6050_conv()
            
        except:
            pass

        self.temp_angle += (wz + 0.436) * (time.time() - self.last_read_time)
        self.last_read_time = time.time()
        time.sleep(0.01)
        return self.temp_angle * -1 
    
    def reset(self):
        self.temp_angle = 0
        
        
if __name__ == "__main__":
    pass
	