import numpy as np
import cv2
import serial
import time


#arduino =  serial.Serial("/dev/ttyACM0", 9600, timeout=1)
#time.sleep(1)
#if arduino.isOpen():
#    print("conected")
    
g_find = False
r_find = False
red_area = 0
green_area = 0


webcam = cv2.VideoCapture(0)
while(1):
    _, imageFrame = webcam.read()
    
    imageFrame = cv2.blur(imageFrame, (10,10))
    imageFrame = cv2.resize(imageFrame,(480,300))
    
    imageFrame = cv2.flip(imageFrame,0)
  
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
    red_lower = np.array([150, 100, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    kernal = np.ones((20,20), "uint8")
      
    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
    
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)
   
    # Creating contour to track red color
    r_contours, r_hierarchy = cv2.findContours(red_mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    g_contours, g_hierarchy = cv2.findContours(green_mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    r_flag = False
    for pic, contour in enumerate(r_contours):
        r_areas = [cv2.contourArea(c) for c in r_contours]
        max_index = np.argmax(r_areas)
        cnt=r_contours[max_index]
        M = cv2.moments(contour)
        r_area = cv2.contourArea(contour)
        
        if(r_area > 1000):
            x, y, w, h = cv2.boundingRect(cnt)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            r_cw = int(M['m10']/M['m00'])
            red_area = h * w
            r_flag = True
        
            

    g_flag = False
    for pic, contour in enumerate(g_contours):
        g_areas = [cv2.contourArea(c) for c in g_contours]
        max_index = np.argmax(g_areas)
        cnt=g_contours[max_index]
        M = cv2.moments(contour)
        g_area = cv2.contourArea(contour)
        green_area = 0 
        if(g_area > 1000):
            x, y, w, h = cv2.boundingRect(cnt)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            g_cw = int(M['m10']/M['m00'])
            green_area = h * w
            g_flag = True



    # Program Termination
    if not r_flag and not g_flag:
        cmd = 0
   
    elif r_flag and green_area <= red_area :
        cmd = (r_cw / 50) - 2     
        cmd = round(cmd * (red_area/5000)* -1)
        
    elif g_flag and green_area >= red_area :
        g_cw = abs(480 - g_cw)
        cmd = (g_cw / 50) - 2      
        cmd = round(-cmd * (green_area/5000) )
    else:
        cmd = 0
        
        
    #arduino.write(str(cmd*5).encode())
    print(cmd)
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)




    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break