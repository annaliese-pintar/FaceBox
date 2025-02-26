import cv2 
import face_recognition
import time
import os

def my_function():

    start_time = time.time()

    recognized = False

    # begin video capture
    video_capture = cv2.VideoCapture(0); # default cam 

    image_folder = "model"
    image_name = "my_image.jpeg"
    image_path = os.path.join(image_folder, image_name)


    # picture of me
    my_picture = face_recognition.load_image_file(image_path)
    my_face_encoding = face_recognition.face_encodings(my_picture)[0]

    while time.time() - start_time < 30:
        result, frame = video_capture.read() # capture each frame 

        # if frame is not read successfully, terminate loop
        if result is False:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert BGR to RGB

        face_location = face_recognition.face_locations(rgb_frame)
        face_encoding = face_recognition.face_encodings(rgb_frame, face_location)

        for top, right, bottom, left in face_location:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            found = face_recognition.compare_faces(my_face_encoding, face_encoding)
            if True in found:
                recognized = True
                print("It's ME!!!")
                
        cv2.imshow('Face Recognition', frame)

        if recognized is True:
            break
        



        # press 'q' to exit 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(1)

    return recognized


    video_capture.release()
    cv2.destroyAllWindows()