import cv2
import face_recognition 

# load an image file 
image = face_recognition.load_image_file("my_image.jpeg")

# find all face locations in image 
face_locations = face_recognition.face_locations(image)

print(f"Found {len(face_locations)} face(s) in this photograph.")