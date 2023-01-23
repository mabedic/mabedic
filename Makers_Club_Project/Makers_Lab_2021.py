import cv2
import numpy as np
import RPI.GPIO as GPIO 
from time import sleep

servoPin          = 12   
SERVO_MAX_DUTY    = 12   
SERVO_MIN_DUTY    = 3    

GPIO.setmode(GPIO.BOARD)       
GPIO.setup(servoPin, GPIO.OUT)  

servo = GPIO.PWM(servoPin, 50)
servo.start(0)

def setServoPos(degree):
    if degree > 180:
      degree = 180

    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
    print("Degree: {} to {}(Duty)".format(degree, duty))

    servo.ChangeDutyCycle(duty)

thresh = 25

a, b, c = None, None, None

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

while cv2.waitKey(27) < 0:
    ret, a = cap.read()
    a_crop = a[120:200, 160:320]
    ret, b = cap.read()
    ret, c = cap.read()
    #cv2.imshow("a_crop", a_crop)
    #if not cap.isOpened:
        #break

    a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    
    diff1 = cv2.absdiff(a_gray, b_gray)
    diff2 = cv2.absdiff(b_gray, c_gray)
    
    ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
    ret, diff2_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
    
    diff = cv2.bitwise_and(diff1_t, diff2_t)
    
    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)
    
    diff_cnt = cv2.countNonZero(diff)

    cv2.rectangle(a, (160,120), (320,200), (0,255,0), 2)
    cv2.imshow("Moniter", a)

    if diff_cnt < 1:
        print("NOT MOTION")

        lower_red = np.array([160, 50, 50])
        upper_red = np.array([180, 255, 255])

        dst_red = cv2.cvtColor(a_crop, cv2.COLOR_BGR2HSV)
        red_img = cv2.inRange(dst_red, lower_red, upper_red)

        red_cnt = cv2.countNonZero(red_img)
        #print(str(red_cnt))

        if red_cnt > 5:
            print("RED")
            setServoPos(0)
            sleep(1)
            setServoPos(30)
            sleep(1)
            setServoPos(-10)
            sleep(1)
            #servo.stop()

    else:
        print("MOTION")
