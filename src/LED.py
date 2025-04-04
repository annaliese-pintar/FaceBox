import RPi.GPIO as GPIO
from time import sleep

# will refer to the GPIO pins by the number directly after the word GPIO
GPIO.setmode(GPIO.BCM)
# prevents warning if still active from previous time the code was run
GPIO.setwarnings(False)

def green_LED_on():
    # sets GPIO 23 pin as an output pin 
    GPIO.setup(23, GPIO.OUT)
    # turn on green LED
    GPIO.output(23, 1)
    
def green_LED_off():
    # sets GPIO 23 pin as an output pin 
    GPIO.setup(23, GPIO.OUT)
    # turn off green LED
    GPIO.output(23, 0)
    
def red_LED():
    # sets GPIO 24 pin as an output pin 
    GPIO.setup(24, GPIO.OUT)
    # red LED blinks 3 times
    GPIO.output(24, 1)
    sleep(1)
    GPIO.output(24, 0)
    sleep(0.5)
    GPIO.output(24, 1)
    sleep(1)
    GPIO.output(24, 0)
    sleep(0.5)
    GPIO.output(24, 1)
    sleep(1)
    GPIO.output(24, 0)
    
    
