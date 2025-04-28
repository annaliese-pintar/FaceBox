# FaceBox

## How It Works
FaceBox is a box that opens with facial recognition. The python application for this project runs on a Raspberry Pi 4, which controls the solenoid that holds the box shut, the camera module for live video feed, and the two LED lights that indicate the state of the application. The application automatically starts when the Raspberry Pi turns on. When the application starts, the green LED turns on. The camera module provides live feed for the application to visualize a face and compare it to the image provided. If the face matches the face in the image, the solenoid will release the latch and the box will be opened. If the face does not match the provided image, the red LED will blink three times. At the end of the application, the green LED will turn off and the Raspberry Pi auomatically shuts off.

### Video showing how the box works:
[![Video explaining the box](https://img.youtube.com/vi/-yx-T_3bWLI/0.jpg)](https://youtu.be/-yx-T_3bWLI)

## What You Will Need To Build FaceBox
### Materials 
* [Raspberry Pi 4](https://a.co/d/dmxZY0r)
    - [Raspberry Pi power switch](https://a.co/d/eeoZahd) (if you don't buy the kit)  
* [Camera module with case](https://a.co/d/2vhtAw)
* [12V Electronic solenoid door lock](https://a.co/d/dyk63Oi)
* [5V Relay](https://a.co/d/dMmcy7T)
* 2 [Rechargeable Lithium ion battery packs](https://a.co/d/iqWXyzS)
* [Power adapter](https://a.co/d/6XaGGVK)
* [Jumper ribbon cables](https://a.co/d/10DB8zA)
* Green LED
* Red LED
* 2 Resistors (calculate appropriate resistor using Ohm's Law)
* [Box](https://a.co/d/5UvDAct)
* Screws to secure the solenoid to the box of your choice
* Hot Glue
* Wood Glue
* Paint stir sticks (depending on the box you use)

### Tools
* Drill
* Hot glue gun
* Wood chisels
* Rubber mallet
* Hand saw
* Portable quick clamp
* Bar clamp

## How It's Made
### Software 
You will need to install:
* OpenCV
* Picamera2
* face_recognition

Instruction for installation will vary by operating system so I recommend google how to install the above packeges for your OS.

You can test everything is installed correctly with this code:
```
# test_installation.py
import cv2
import face_recognition
from picamera2 import Picamera2

# Just import to check
print("OpenCV version:", cv2.__version__)
print("Face recognition imported successfully")
print("Picamera2 imported successfully")

# Initialize camera to test
picam2 = Picamera2()
print("Camera initialized successfully")

print("All libraries installed correctly!")
```

### Electrical  
![Electrical diagram for the facial recotgnition box](/faceboxdiagram.png)
