import facial_recognition
import lock_control
import LED
import os

if facial_recognition.recognise_face() is True:
    lock_control.lock_function()
    LED.green_LED()
else:
    LED.red_LED()

# shut down pi
# os.system("sudo shutdown -h now")
