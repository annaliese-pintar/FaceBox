# FaceBox

## How It Works
FaceBox is a box that opens with facial recognition. The python application for this project runs on a Raspberry Pi 4, which controls the solenoid that holds the box shut, the camera module for live video feed, and the two LED lights that indicate the state of the application. The application automatically starts when the Raspberry Pi turns on. When the application starts, the green LED turns on. The camera module provides live feed for the application to visualize a face and compare it to the image provided. If the face matches the face in the image, the solenoid will release the latch and the box will be opened. If the face does not match the provided image, the red LED will blink three times. At the end of the application, the green LED will turn off and the Raspberry Pi auomatically shuts off.

## What You Will Need To Build FaceBox
### Materials 
* Camera module with case - https://a.co/d/2vhtAwm

### Tools

## How It's Made
### Software 

### Hardware 
