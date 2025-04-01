# Start with Python base image
FROM python:3.9-slim-bullseye

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Add Raspberry Pi OS repository
RUN apt-get update && apt-get install -y gnupg wget apt-transport-https

# Add Raspberry Pi OS repository with modern gpg key handling
RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" > /etc/apt/sources.list.d/raspi.list
RUN wget -O - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | gpg --dearmor > /etc/apt/trusted.gpg.d/raspberrypi.gpg

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libv4l-dev \
    pkg-config \
    libcap-dev \
    python3-opencv \
    python3-picamera2 \
    python3-libcamera \
    python3-rpi.gpio \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install face_recognition and other Python packages
RUN pip install --no-cache-dir \
    numpy \
    dlib \
    face_recognition

# Create directory structure
WORKDIR /app
RUN mkdir -p /app/model

# Copy application files
COPY *.py /app/
COPY model/ /app/model/

# Run the application
CMD ["python3", "pi_setup.py"]