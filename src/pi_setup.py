import facial_recognition
import lock_control
import LED
import os
import safe_control

# turn on green LED at the start of the application 
LED.green_LED_on()

try:
    if facial_recognition.recognise_face() is True:
        lock_control.lock_function()

    else:
        LED.red_LED()
    
finally:
    # turn off green LED at the end of the application
    LED.green_LED_off()

# shut down pi
if safe_control.safe_shutdown():
    os.system("sudo shutdown -h now")
