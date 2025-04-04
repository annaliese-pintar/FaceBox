import RPi.GPIO as GPIO
from time import sleep

def lock_function():
    print("IN LOCK FUNCTION")
    # prevents warning if still active from previous time the code was run
    GPIO.setwarnings(False)

    # will refer to the GPIO pins by the number directly after the word GPIO
    GPIO.setmode(GPIO.BCM)

    # sets GPIO 18 pin as an output pin 
    GPIO.setup(18, GPIO.OUT)
    
    
    GPIO.output(18, 0)  
    
    sleep(0.1)     
    
    GPIO.output(18, 1)
    
    sleep(0.1)
    
    GPIO.cleanup(18)
                                            
