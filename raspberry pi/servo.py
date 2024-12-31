import RPi.GPIO as GPIO
import time

def servo_motor(pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)
    
    # Start PWM with 1% duty cycle
    pwm.start(1)
    

    time.sleep(1)
    
    # Change to 12% duty cycle
    pwm.ChangeDutyCycle(12)
    

    time.sleep(1)
    

    pwm.stop()

if __name__ == "__main__":
    servo_motor(17)  

