#!/bin/bash

# This script helps test if the container has access to all necessary hardware

# Make sure script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

echo "Building container..."
docker-compose build

echo "Starting container for testing..."
docker-compose run --rm facial-recognition-box bash -c "
echo '===== TESTING HARDWARE ACCESS =====';
echo '';

echo '--- Testing Python and imports ---';
python3 -c 'import sys; print(f\"Python version: {sys.version}\")';
python3 -c 'import cv2; print(f\"OpenCV version: {cv2.__version__}\")';
python3 -c 'import numpy; print(f\"NumPy version: {numpy.__version__}\")';
python3 -c 'import face_recognition; print(\"face_recognition imported successfully\")' || echo 'face_recognition import failed';
python3 -c 'import picamera2; print(f\"picamera2 imported successfully\")' || echo 'picamera2 import failed';
python3 -c 'import RPi.GPIO as GPIO; print(\"RPi.GPIO imported successfully\")' || echo 'RPi.GPIO import failed';

echo '';
echo '--- Testing camera access ---';
ls -la /dev/vchiq || echo 'Camera device not found';
vcgencmd get_camera || echo 'vcgencmd not available';

echo '';
echo '--- Testing GPIO access ---';
ls -la /dev/gpiomem || echo 'GPIO device not found';

echo '';
echo 'If all tests passed, your container should be able to access all required hardware';
"