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
#### Code Adjustments Depending On Relay Trigger Mode
It is important to know the trigger mode of your relay. The mode can be either active-high/high-level trigger or active-low/low-level trigger. If it is active-high, it will activate when the control pin receives a high signal (5V), while if it is active-low, it will activate when the control pin is set to LOW (0V). The relay I used is active-low. If you are using an active-high relay, you will have to make some changes to the lock_control.py file:

```
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
    
    
    GPIO.output(18, 1)  
    
    sleep(0.1)     
    
    GPIO.output(18, 0)
    
    sleep(0.1)
    
    GPIO.cleanup(18)

```

> [!CAUTION]
> Setting the GPIO pins to the incorrect output for your relay's trigger mode can cause overheating and damage to the solenoid depending on the solenoid used. [Learn from my mistakes.](#trigger-mode-mistake)

> [!CAUTION]
> Be aware of the limit to the amount of time your solenoid can be powered. If the solenoid recieves power longer than its limits, it can overheat and damage the solenoid. [Learn from my mistakes](#sleep-time-mistake)

### Create Development Mode and Production Mode Flags
Since the pi automatically shuts off at the end of the application, we will need some way to prevent the pi from shutting off in the event you want to make changes to the application. We are going to use a file flag to put the application into development mode. During the shut down process there is a 10 second countdown and during the countdown the application checks if the dev_mode file exists. If it does exist, the safe_shutdown function in the safe_control.py file will return false and the pi will not shut down. We will create a development mode and production mode file that will contain scripts to remotely (from your computer) add and remove a dev_mode file from the src directory on your pi. You will need to enable SSH on your pi before we make the script files.

#### Enable SSH On Your Pi
1. Open a terminal
2. Enable SSH permanently:
```
sudo systemctl enable ssh
sudo systemctl start ssh
```
3. Verify SSH is running:
```
sudo systemctl status ssh
```
4. Test SSH connection from you PC (replace pi with your pi's name and replace your-pi-ip with your pi's IP address):
```
ssh pi@your-pi-ip
```

#### Windows
##### Development Mode Flag
1. Open PowerShell on your Windows computer
2. Navigate to where you want to create the file (recommend home directory):
```
cd ~
```
3. Use the Set-Content cmdlet to create the file with contents (Replace 192.168.1.100 with your Pi's actual IP address and pi with your pi's name):
```
Set-Content -Path .\pi-dev-mode.ps1 -Value @'
ssh pi@192.168.1.100 "touch /home/pi/FaceBox/src/dev_mode"
Write-Host "Development mode enabled on Raspberry Pi" -ForegroundColor Green
'@
```
4. Verify the file was created:
```
Get-Content .\pi-dev-mode.ps1
```

Now the script is ready to use. If you want to turn on development mode (prevent the pi from shutting off automatically), while the pi is on, open a PowerShell on your PC and type:
```
.\pi-dev-mode.ps1
```
It should then prompt you to enter the password for your Raspberry Pi.

##### Production Mode (Remove Flag)
1. Open PowerShell on your Windows computer
2. Navigate to where you want to create the file (recommend home directory):
```
cd ~
```
3. Use the Set-Content cmdlet to create the file with contents (Replace 192.168.1.100 with your Pi's actual IP address and pi with your pi's name):
```
Set-Content -Path .\pi-prod-mode.ps1 -Value @'
ssh pi@192.168.1.100 "rm /home/pi/FaceBox/src/dev_mode"
Write-Host "Production mode enabled on Raspberry Pi" -ForegroundColor Green
'@
```
4. Verify the file was created:
```
Get-Content .\pi-prod-mode.ps1
```

Now the script is ready to use. If you want to turn on production mode (allow the pi to shut off automatically), while the pi is on, open a PowerShell on your PC and type:
```
.\pi-prod-mode.ps1
```

It should then prompt you to enter the password for your Raspberry Pi.

#### Mac
##### Development Mode Flag
1. Open Terminal on your MacBook
2. Navigate to where you want to create the file (recommend home directory):
```
cd ~
```
3. Create the file using a text editor like nano:
```
nano pi-dev-mode.sh
```
4. In the nano editor, type the script (replace YOUR_PI_IP with your actual Pi's IP address and pi with your pi's name):
```
#!/bin/bash
ssh pi@YOUR_PI_IP "touch /home/pi/FaceBox/src/dev_mode"
echo "Development mode enabled on Raspberry Pi"
```
5. Save the file by pressing Ctrl+X, then Y, then Enter
6. Make the file executable:
```
chmod +x pi-dev-mode.sh
```

Now the script is ready to use. If you want to turn on development mode (prevent the pi from shutting off automatically), while the pi is on, open a terminal on your Mac and type:
```
./pi-dev-mode.sh
```
It should then prompt you to enter the password for your Raspberry Pi.

##### Production Mode (Remove Flag)
1. Open Terminal on your MacBook
2. Navigate to where you want to create the file (recommend home directory):
```
cd ~
```
3. Create the file using a text editor like nano:
```
nano pi-prod-mode.sh
```
4. In the nano editor, type the script (replace YOUR_PI_IP with your actual Pi's IP address and pi with your pi's name):
```
#!/bin/bash
ssh pi@YOUR_PI_IP "rm /home/pi/FaceBox/src/dev_mode"
echo "Production mode enabled on Raspberry Pi"
```
5. Save the file by pressing Ctrl+X, then Y, then Enter
6. Make the file executable:
```
chmod +x pi-prod-mode.sh
```

Now the script is ready to use. If you want to turn on development mode (prevent the pi from shutting off automatically), while the pi is on, open a terminal on your Mac and type:
```
./pi-prod-mode.sh
```
It should then prompt you to enter the password for your Raspberry Pi.

### Create the service file on Raspberry Pi 4B
The facebox.service file will allow for you to create a service that automatically starts the application when the Raspberry Pi boots up.

1. In terminal on the Raspberry Pi type:
```
sudo nano /etc/system/facebox.service
```
2. In the nano editor, type the script (replace all instances of pi with pi's name):
```
[Unit]
Description=Face Recognition Box
After=network.target

[Service]
ExecStart=/home/pi/FaceBox/src/path/to/venv/bin/python /home/pi/FaceBox/src/pi_setup.py
WorkingDirectory=/home/pi/FaceBox/src
StandardOutput=journal        
StandardError=journal
Restart=no
User=pi

[Install]
WantedBy=multi-user.target
```
3. Save the file and reload systemd:
```
sudo systemctl daemon-reload
```
4. Start the service:
```
sudo systemctl start facebox.service
```
5. Check the status of the service:
```
sudo systemctl status facebox.service
```

### Electrical  
![Electrical diagram for the facial recognition box](/faceboxdiagram.png)

## Mistakes To Learn From
### Trigger Mode Mistake
<a name="trigger-mode-mistake"></a>
While implementing the solenoid, I was not aware that the trigger mode of my relay was active-low. My GPIO pin output was set to HIGH to trigger the relay and then set back to LOW to turn off the relay. However, since my relay's trigger  mode was active-low, I was leaving my relay in an active state rather than returning it to inactive. This caused my solenoid to burn out due to the solenoids 0.2 second limit on how long it should recieve power.

### Sleep Time Mistake
<a name="sleep-time-mistake"></a>
Prior to implementing solenoid controls, I did not fully read the documentation for the solenoid I was using. The documenation states that the solenoid should be powered for only 0.2 seconds max. In between my GPIO pin controls for setting the ouput from LOW back to HIGH I have a sleep function. Initally, I set the sleep function to sleep for 1 second leaving the GPIO pin output on LOW for 1 second which means that solenoid was powered longer than it's max causing the solenoid to burn out.
