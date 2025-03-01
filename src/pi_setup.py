import facial_recognition
import lock_control
import LED

if facial_recognition.recognise_face() is True:
    lock_control.lock_function()
    LED.green_LED()
else:
    LED.red_LED()