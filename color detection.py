import numpy as np
import cv2
import RPi.GPIO as GPIO
import serial
import time

# x coordinate
# y coordinate
# w : width
# h : height
# z : erea of rectangle
# 630
r_cw = 0

arduino =  serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(1)
if arduino.isOpen():
    print("conected")
g_area = 0
g_cw = -1
r_area = 0
r_cw = -1
#pos.reset_input_buffer()

webcam = cv2.VideoCapture(0)
while(1):
    cmd = ""
    _, imageFrame = webcam.read()
    imageFrame = cv2.flip(imageFrame,0)
  
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    kernal = np.ones((5, 5), "uint8")
      
    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
    
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)
   
    # Creating contour to track red color
    r_contours, r_hierarchy = cv2.findContours(red_mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    g_contours, g_hierarchy = cv2.findContours(green_mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    r_area = 0;
    r_cw = -1
    for pic, contour in enumerate(r_contours):
        r_areas = [cv2.contourArea(c) for c in r_contours]
        max_index = np.argmax(r_areas)
        cnt=r_contours[max_index]
        M = cv2.moments(contour)
        r_area = cv2.contourArea(contour)
        if(r_area > 300):
            x, y, w, h = cv2.boundingRect(cnt)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
              
            cv2.putText(imageFrame, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))    
            #cx = int(M['m10']/M['m00'])
            #cy = int(M['m01']/M['m00'])
            r_cw = int(M['m10']/M['m00'])
            r_ch = int(M['m01']/M['m00'])
            #r_area = h
        #else:
         #   r_area = 0
        
            

    
    for pic, contour in enumerate(g_contours):
        g_areas = [cv2.contourArea(c) for c in g_contours]
        max_index = np.argmax(g_areas)
        cnt=g_contours[max_index]
        M = cv2.moments(contour)
        g_area = cv2.contourArea(contour)
        if(g_area > 300):
            x, y, w, h = cv2.boundingRect(cnt)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
              
            cv2.putText(imageFrame, "Green Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 255, 0))    
            #cx = int(M['m10']/M['m00'])
            #cy = int(M['m01']/M['m00'])
            g_cw = int(M['m10']/M['m00'])
            g_ch = int(M['m01']/M['m00'])
        else:
            g_area = 0



    # Program Termination
    cmd = 0
    if g_area <= r_area and r_area != 0 :
        if r_cw <= 100:
            cmd = 0
        elif r_cw <= 150:
            cmd = 1
        elif r_cw <= 250:
            cmd = 2
        elif r_cw <= 300:
            cmd = 3
        elif r_cw <= 300:
            cmd = 4
        elif r_cw <= 350:
            cmd = 5
        elif r_cw <= 400:
            cmd = 6
        elif r_cw <= 500:
            cmd = 7
        elif r_cw <= 600:
            cmd = 8
        elif r_cw >= 600:
            cmd = 9
            r_area = 20000
        cmd = cmd * (r_area/10000)
        
    if g_area >= r_area and g_area != 0 :
        g_cw = abs(650 - g_cw)
        if g_cw >= 0 and g_cw < 150:
            cmd = 0
        elif g_cw <= 150:
            cmd = 1
        elif g_cw <= 250:
            cmd = 2
        elif g_cw <= 300:
            cmd = 3
        elif g_cw <= 350:
            cmd = 4
        elif g_cw <= 400:
            cmd = 5
        elif g_cw <= 450:
            cmd = 6
        elif g_cw <= 500:
            cmd = 7
        elif g_cw <= 600:
            cmd = 8
        elif g_cw >= 600:
            cmd = 9
            g_area = 20000
            
        cmd *= -1
        cmd = cmd * (g_area/10000)
        
    #print(cmd)
    cmd = round(cmd)
    arduino.write(str(cmd).encode())
    print(cmd)
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break