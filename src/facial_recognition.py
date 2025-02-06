import cv2 
import face_recognition

# begin video capture
video_capture = cv2.VideoCapture(0); # default cam 

# picture of me
my_picture = face_recognition.load_image_file('my_image.jpeg')
my_face_encoding = face_recognition.face_encodings(my_picture)[0]

while True:
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
            print("It's ME!!!")
    cv2.imshow('Face Recognition', frame)

    


    # press 'q' to exit 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video_capture.release()
cv2.destroyAllWindows()