import cv2 
import face_recognition
import time
import os
from picamera2 import Picamera2

def recognise_face():
    print("IN RECOGNISE_FACE")
    start_time = time.time()

    recognized = False

    # begin video capture
    # video_capture = cv2.VideoCapture(0); # default cam 
    # print(video_capture.isOpened())
    # print(video_capture.read())
    
    # initialize the picamera2
    print("Initializing camera...")
    picam2 = Picamera2()
    
    #configure cam 
    preview_config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
        
    picam2.configure(preview_config)
    
    picam2.start() 
    print("Camera started")
    
    time.sleep(2)

    print("Loading reference image...")
    image_folder = "model"
    image_name = "my_image.jpeg"
    image_path = os.path.join(image_folder, image_name)

    try:
        # picture of me
        print(f"Loading image from: {image_path}")
        my_picture = face_recognition.load_image_file(image_path)
        print("Reference image loaded, encoding face...")
        my_face_encoding = face_recognition.face_encodings(my_picture)[0]
        print("Face encoded successfully")
    except Exception as e:
        print(f"Error with reference image: {e}")
        picam2.stop()
        return False
    
    try:
        print("Entering recognition loop...")
        while time.time() - start_time < 30:
            # capture frame
            frame = picam2.capture_array()
            #("Frame captured")
            
            # resize frame to 1/4 size for faster processing 
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            #print("Frame resized")
            
            # Convert BGR to RGB (face_recognition uses RGB)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            #print("Frame converted to RGB")
            
            # find face locations
            #print("Finding face locations...")
            face_locations = face_recognition.face_locations(rgb_small_frame)
            #print(f"Found {len(face_locations)} faces")
            
            # Only encode if we found faces
            if face_locations:
                print("Encoding detected faces...")
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                print("Faces encoded")
                
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    print("Comparing faces...")
                    # Compare faces
                    matches = face_recognition.compare_faces([my_face_encoding], face_encoding)
                    
                    if True in matches:
                        recognized = True
                        print("It's ME!!!")
            
            
            if recognized:
                print("Face recognized! Exiting loop.")
                break
            
                
            time.sleep(0.1)  # Small delay to reduce CPU usage
            
    except Exception as e:
        print(f"Error in recognition loop: {e}")
    finally:
        # Always clean up
        print("Cleaning up resources...")
        picam2.stop()

        
    return recognized
