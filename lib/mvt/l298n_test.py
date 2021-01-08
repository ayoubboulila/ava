import RPi.GPIO as GPIO
from time import sleep
def stop(m1, m2):
    print("stopping motors")
    m1.ChangeDutyCycle(0)
    m2.ChangeDutyCycle(0)
    
try:
    GPIO.setmode(GPIO.BCM)

    en,in1,in2 = 26,19,13
    enb,in3,in4 = 9,6,5

    GPIO.setup(en,GPIO.OUT)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    pwm = GPIO.PWM(en,100)
    pwm.start(0)
    
    GPIO.setup(enb,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    pwm2 = GPIO.PWM(enb,100)
    pwm2.start(0)
    while True:
        print("moving back")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        pwm.ChangeDutyCycle(100)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        pwm2.ChangeDutyCycle(100)
        sleep(4)
        stop(pwm, pwm2)
        print("moving forward")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        pwm.ChangeDutyCycle(100)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        pwm2.ChangeDutyCycle(100)
        sleep(4)
        stop(pwm, pwm2)
        
        print("moving right")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        pwm.ChangeDutyCycle(100)
        pwm2.ChangeDutyCycle(0)
        sleep(4)
        stop(pwm, pwm2)
        
        print("moving left")
        
        pwm.ChangeDutyCycle(0)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        pwm2.ChangeDutyCycle(100)
        sleep(4)
        stop(pwm, pwm2)
        

except KeyboardInterrupt:
    print("interrupt")
except:
    print("exception")
finally:
    GPIO.cleanup()
