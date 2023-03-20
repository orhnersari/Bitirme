#!/usr/bin/env python
# /etc/init.d/main.py
### BEGIN INIT INFO
# Provides:          main.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon
### END INIT INFO
 
from PIL import Image, ImageFilter
import numpy as np
import cv2
import time
import RPi.GPIO as GPIO          
from time import sleep
import serial
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

in1 = 13
in2 = 15
ena = 16
enb = 18

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

pwm = GPIO.PWM(enb,1000)
pwm.start(25)

uart_channel = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0)
renk = ""  
ilkKomut = ""
sonKomut = ""
skor = 0

a=0
b=0
c=0
d=0


def ileri():#sag
    #print("Motorar ileri gidiyor")
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    # GPIO.output(ena,GPIO.HIGH)
    # GPIO.output(enb,GPIO.HIGH)
    pwm.ChangeDutyCycle(100)
    

def geri():#sol
    #rint("Motorar geri gidiyor")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    # GPIO.output(ena,GPIO.HIGH)
    # GPIO.output(enb,GPIO.HIGH)
    pwm.ChangeDutyCycle(100)

def dur():
    #print("Motorar durdu")   
    #GPIO.output(ena,GPIO.LOW)
    #GPIO.output(enb,GPIO.LOW)

    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    #pwm.ChangeDutyCycle(0)


def Basla():
    uart_channel.write(b"baslamak icin start komutu veriniz")
    while True:
        ilkKomut = uart_channel.read(10)
        #print('basladi')
        if(ilkKomut==b"start"):
            return 1
        
def Giris():

    uart_channel.write(b"kirmizi mi yesil mi")
    while True:
        renk = uart_channel.read(10)
        if renk == b"yesil":
            return 1
        elif renk == b"kirmizi":
            return 0

    # uart_channel.write(b"kirmizi mi yesil mi")
    # while True: 
    #     renk = uart_channel.read(10)  
    
    #     if renk == "yesil":
    #         print('giris yesil func')
    #         return 1
    #     elif renk == "kirmizi":
    #         print('giris kirmizi func')
    #         return 0  

def Bitir():
     
    
     sonKomut = uart_channel.read(10)
     if sonKomut == b"bitir":
        GPIO.cleanup()
        return 1 
     else :
        return 0




# Set range for red color
red_lower = np.array([158, 70, 20], np.uint8) # 158, 70, 20    0, 100, 20
red_upper = np.array([179, 255, 255], np.uint8) # 179, 255, 255    10, 255, 255
# red_lower = np.array([160,95,20], np.uint8) # 160, 95, 20     160,100,20
# red_upper = np.array([179,255,255], np.uint8) # 179, 255, 255

# Set range for green color
green_lower = np.array([40, 78, 128], np.uint8) # 40, 78, 128
green_upper = np.array([90, 255, 255], np.uint8) # 90, 255, 255

# Set range for blue
blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)

#Set range for yellow
yellow_lower = np.array([20, 100, 100], np.uint8)
yellow_upper = np.array([300, 255, 255], np.uint8)

# Set range for led
lower_led = np.array([0, 0, 230], np.uint8)
upper_led = np.array([179, 255, 255], np.uint8)

# Set range for led light
lower_light = np.array([0, 120, 130], np.uint8)
upper_light = np.array([179, 255, 255], np.uint8)

# Morphological Transform, Dilation for each color and bitwise_and operator
# between imageFrame and mask determines to detect only that particular color
kernel = np.ones((5,5), np.uint8)
kernal = np.ones((3, 3), np.uint8)
kernal2 = np.ones((20, 20), np.uint8)
kernal3 = np.ones((2, 2), np.uint8)

sayac = 0
sayac2 = 0
takip = Giris()

#baslaKomutu = Basla()
# Capturing video through webcam

komut = Basla()
# if(baslamaKomutu == 1):
#     bir = 1
# else:
#     bir = 0

# Start a while loop
#sonKomut = 
webcam = cv2.VideoCapture(0)
while(komut):
    
    sonkomut = Bitir()
    
    if(sonkomut==1):        
        uart_channel.write(b"oyun bitti skorunuz ")
        uart_channel.write(str(skor).encode('ascii'))
        break
    #Reading the video from the webcam in image frames
    #print('girdi')
    _, frame = webcam.read()
    try:
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(str(e))

    raw = frame.shape[1] / 2
    column = frame.shape[0] / 2
    # Convert the imageFrame in BGR(RGB color space) to
    # HSV(hue-saturation-value)color space
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    # Red Thresholding
    #lower_mask = cv2.inRange(hsvFrame, red_lower_b, red_upper_b)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    #red_mask = lower_mask + upper_mask
 
    # Green Thresholding
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Blue Thresholding
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
   
    # Led Thresholding
    led_mask = cv2.inRange(hsvFrame, lower_led, upper_led)

    # Led Light Thresholding
    ledLight_mask = cv2.inRange(hsvFrame, lower_light, upper_light)

    bitwiseOr = cv2.bitwise_or(ledLight_mask, led_mask)
    opening = cv2.morphologyEx(bitwiseOr, cv2.MORPH_OPEN, kernel)
     
    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernal2)
     
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernal2)

    bitwiseOr = cv2.dilate(bitwiseOr, kernal3)
    bitwiseOr = cv2.morphologyEx(bitwiseOr, cv2.MORPH_CLOSE, kernal3)

    red_mask = cv2.bitwise_and(bitwiseOr, red_mask)
    green_mask = cv2.bitwise_and(bitwiseOr, green_mask)
     
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
   
    y_r_max = 0
    x_r_array = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 75):
            x, y, w, h = cv2.boundingRect(contour)
            x_r_array.append(x)
            if((y+h)-y_r_max >= 0):
                y_r_max = y + h
                x_r_max = x + round(w/2)
           
            # cv2.circle(frame,( x + round(w/2) , y + h),5,255,-1)
    if(y_r_max != 0):
       cv2.circle(frame,( x_r_max , y_r_max ),5,255,-1)          
 
    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    y_g_max = 0
    x_g_array = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 75):
            x, y, w, h = cv2.boundingRect(contour)
            x_g_array.append(x)
            if((y+h)-y_g_max > 0):
                y_g_max = y + h
                x_g_max = x + round(w/2)
           
           
            #cv2.circle(frame,( x + round(w/2), y + h),5,255,-1)
            # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
   
    y_blue = 0
    x_aralar = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 150):
            x, y, w, h = cv2.boundingRect(contour)
            x_aralar.append(x)
            if ( y > y_blue ):
                 y_blue = y
                 x_cikart = x
            
            M = cv2.moments(contour)
            cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
 
   
    if (takip == 1): #Yesil
        #print(y_g_max)
        if(abs(y_r_max - y_blue) < 20 and abs(x_r_max - raw) < 40):
           sayac2 = sayac2 + 1
        else:
            skor = skor - round(sayac2/30)
            #print(skor)
            sayac2 = 0
        if(y_g_max != 0):
            #print(x_g_max)
            if(abs(x_g_max - raw) < 40):
               #print('motorlari durdur')
               dur()
               if(abs(y_g_max - y_blue) < 20 ):
                  sayac = sayac + 1
                  #print(sayac)
            else:
               skor = skor + 2*round(sayac/30)     
        
               if(( raw - x_g_max) < 0):
                  #print('saga hareket')
                  ileri()
               else:
                  #print('sola hareket')
                  geri()
               sayac = 0
               #print(skor)
        else:
            #print('yesil yok')
            if(abs(raw - x_r_max) < 40):
                #print('motorlar saga')
                ileri()
            else:
                #print('motorlari durdur')
                dur()

            if(abs(y_r_max - y_blue) < 20 and abs(x_r_max - raw) < 40):
               sayac2 = sayac2 + 1
            else:
               skor = skor - round(sayac2/30)
               #print(skor)
               sayac2 = 0
            #print(skor)

    if (takip == 0): # kirmizi
        #print(y_g_max)
        if(abs(y_g_max - y_blue) < 20 and abs(x_g_max - raw) < 40):
           sayac2 = sayac2 + 1
        else:
            skor = skor - round(sayac2/30)
            #print(skor)
            sayac2 = 0
        if(y_r_max != 0):
            #print(x_g_max)
            if(abs(x_r_max - raw) < 40):
               #print('motorlari durdur')
               dur()
               if(abs(y_r_max - y_blue) < 20 ):
                  sayac = sayac + 1
                  #print(sayac)
                   
            else:
               skor = skor + 2*round((sayac/30))
               #print(sayac)
               if(( raw - x_r_max) < 0):
                  #print('saga hareket')
                  ileri()
               else:
                  #print('sola hareket')
                  geri()
               sayac = 0
               #print(skor)
        else:
            #print('kirmizi yok')
            if(abs(raw - x_g_max) < 40):
                #print('motorlar saga')
                ileri()
            else:
                #print('motorlari durdur') 
                dur() 

            if(abs(y_g_max - y_blue) < 20 and abs(x_g_max - raw) < 40):
               sayac2 = sayac2 + 1
            else:
               skor = skor - round(sayac2/30)
               #print(skor)
               sayac2 = 0  
                
    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", frame)
    cv2.imshow('thresh_green', blue_mask)	        
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
 
