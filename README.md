# FaceBox

## How It Works
FaceBox is a facial recognition-enabled box that unlocks when it recognizes your face. The project runs on a Raspberry Pi 4, which manages three key components: the locking solenoid, the camera module providing live video feed, and two LED indicators that show the system's status. The application launches automatically when the Raspberry Pi powers on, signaled by the green LED illuminating. Using the camera's live feed, the system compares any detected face with the pre-stored reference image. Upon a successful match, the solenoid releases the latch, allowing the box to open. If no match is found, the red LED blinks three times to indicate failure. When the process completes, the green LED turns off and the Raspberry Pi automatically shuts down.

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
* Portable table clamp
* Bar clamp
* Philips head screw driver
* Pencil
* Monitor
* Mouse
* Keyboard

## How It's Made
### Software 
#### Fork A Repository 
To make your own FaceBox, you can fork the repository and clone the forked repository.
[Instructions to forking a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

#### Code Adjustments Depending On Relay Trigger Mode
Understanding your relay's trigger mode is crucial for proper operation. Your relay can be either active-high (high-level trigger) or active-low (low-level trigger). With active-high relays, the control pin requires a high signal (5V) to activate, while active-low relays activate when the control pin receives a LOW signal (0V). The relay I've implemented in this project is active-low. If you're working with an active-high relay instead, you'll need to modify the lock_control.py file accordingly:

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

#### Create Development Mode and Production Mode Flags
Since the Raspberry Pi automatically shuts down when the application ends, you'll need a way to prevent shutdown during development work. We'll implement this using a file flag for development mode. During the shutdown sequence, there's a 10-second countdown where the application checks for the existence of a dev_mode file. If this file exists, the safe_shutdown function in safe_control.py will return false, preventing the Pi from powering off. We'll create both development and production mode script files that will let you remotely add or remove the dev_mode file in the Pi's src directory from your computer. Before setting up these scripts, you'll need to enable SSH on your Raspberry Pi.

##### Enable SSH On Your Pi
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

##### Windows
###### Development Mode Flag
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

###### Production Mode (Remove Flag)
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

##### Mac
###### Development Mode Flag
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

###### Production Mode (Remove Flag)
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

#### Create the service file on Raspberry Pi 4B
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

### Assembling The Box
I got a little over excited when I finally got all the pieces I needed to assemble the box and forgot to take pictures along the way so I will just describe how I went about it. 
 
1. Set up the solenoid:
    1. Line up the solenoid with the center of the front edge of the box and screw it in place with a philips head screws and screw driver 
    2. Place the metal loop that the solenoid latches onto into the solenoid
    3. Measure the distance from the top of the solenoid to the top of the loop's screw plate
    4. Subtract that length from the depth of the top of the lid to get the height of the wooden piece you will add to allow the loop to sit low enough for the solenoid to latch
    5. Glue wooden paint stir sticks together until they match the length calculated above and clamp them together with the bar clamp until they dry
    6. Clamp the dried paint stir stick stack with the portable table clamp and cut a 4 inch long block with the hand saw
    7. Center it along the top edge of the lid of the box, glue it in place and clamp until it dries.
    8. With the metal loop still in the solenoid, close the box until the loops screw plate touches the stir stick block and mark the block where the edges of they plate are.
    9. Unlatch the loop with the solenoid with the emergency unlatchin mechanism (reference solenoid documentation), line it up with the markings on the block and scew it in place with either a drill or screw driver
        
<img src="solenoid.png" alt="solenoid placement" width="350"/>  <img src="loop.png" alt="loop placement" width="350"/>

2. Decide where you want to put the LEDs, mark the placement, and drill holes slightly bigger than the LEDs.

<img src="LED.png" alt="LED placement" width="350"/>

3. Making a hole for the camera module:
    1. Decide where you want to put the camera module and mark the placement by tracing around the case
    2. Drill as many holes as you can inside the marked rectangle
    3. Take the wood chisel and mallet and chisle away the rest of the rectangle

<img src="camera.png" alt="camera placement" width="350"/>

4. Decide where you want to put the battery pack charging ports, mark the placement, and drill holes slightly bigger than the ports
5. Installing the power button:
    1. Decide where you want to put the power button and mark to circles on either side slightly bigger than the c cable ends
    2. Drill the two holes slightly bigger than the c cable ends
    3. Fit the ends of the power button wire through the hole so that the entire power button is on the outside of the box

<img src="powerswitchfront.png" alt="powerswitch placement" width="350"/> <img src="powerswitchback.png" alt="powerswitch placement" width="350"/>

6. Hot glue the LEDs into place
7. Hot glue the charging ports into place
8. Hot glue the camera module into place

## Practical Applications
This build offers versatile applications in various contexts. It could secure keepsakes or create a special surprise for someone special. With minor modifications, it could function as a facial recognition-secured diary. I also see potential for its implementation in escape rooms as an engaging puzzle element. The possibilities for adapting and expanding this build are numerous and worth exploring.

## Possible Improvements 
### Quicker Bootup Time
With the current hardware configuration, the system experiences notably slow bootup times. I'm interested in exploring an alternative to the Raspberry Pi 4 Model B for this project. Specifically, implementing an ESP32-CAM microcontroller would significantly reduce the startup time, making the device more responsive and practical for everyday use.

### Inactive In Poweroff state 
Currently, I power the box by turning on the Raspberry Pi with its power switch, then pressing the button again to completely cut power when finished. If the system could remain in a powered-off state rather than having all power disconnected, it would boot up much faster and eliminate the need to manually press the power switch to turn it off. However, the Raspberry Pi 4B consumes significant power even when shut down. An ESP32-CAM board would be an ideal solution to this problem, offering much lower power consumption in its inactive state.

### Securing Hardware Inside the FaceBox 
For this project, I didn't permanently attach the hardware components to the box since I plan to reuse them in future projects. To make the build more complete and professional, I would secure all components to the bottom of the box and conceal them from view.

### 3D Printed Box 
Customizing a pre-made wooden box was challenging due to my limited tools and woodworking skills, resulting in a less professional finish than desired. For a more tailored solution that properly accommodates and conceals all components, I would design and create a 3D printed enclosure instead.

### Desktop Application
For this project, I'd like to develop a complementary desktop application that enables users to log in, register their box, and update the facial recognition settings. This would allow for more flexible and user-friendly management of the security features.

## Mistakes To Learn From
### Trigger Mode Mistake
<a name="trigger-mode-mistake"></a>
While implementing the solenoid, I wasn't aware that my relay had an active-low trigger mode. I had configured my GPIO pin to output HIGH to activate the relay and then return to LOW to deactivate it. However, since my relay was actually active-low, this configuration had the opposite effect—keeping the relay activated when I thought it was inactive. This critical misunderstanding caused my solenoid to burn out because it received power beyond its 0.2-second operating limit.

### Sleep Time Mistake
<a name="sleep-time-mistake"></a>
Prior to implementing solenoid controls, I didn't fully read the documentation for my solenoid. The documentation clearly states that the solenoid should be powered for a maximum of only 0.2 seconds. Between my GPIO pin control operations that switched the output from LOW back to HIGH, I included a sleep function. Initially, I set this sleep function to pause for 1 second, which kept the GPIO pin output on LOW for a full second. Since this exceeded the solenoid's maximum power duration, it caused the solenoid to burn out.
