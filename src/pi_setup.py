import facial_recognition
import lock_control

if facial_recognition.my_function() is True:
    lock_control.lock_function()
else:
    print("locked")