import RPi.GPIO as GPIO
from time import sleep

def lock_function():
    # prevents warning if still active from previous time the code was run
    GPIO.setwarnings(False)

    # will refer to the GPIO pins by the number directly after the word GPIO
    GPIO.setmode(GPIO.BCM)

    # sets GPIO 18 pin as an output pin 
    GPIO.setup(18, GPIO.OUT)

    # turns relay off and brings voltage to MAX GPIO can output ~3.3V
    GPIO.output(18, 1)
    # wait 1 second 
    sleep(1)
    # turns relay on and brings voltage to MIN GPIO can output ~0v
    GPIO.output(18, 0)                                                    