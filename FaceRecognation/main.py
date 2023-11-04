import face_recognition
import cv2
import numpy as np

# This function will encode the faces from your provided images
def encode_faces(filenames):
    encoded_list = []
    for file in filenames:
        # Load each image
        image = face_recognition.load_image_file(f"myPhotos/{file}")
        # Encode the face in the image and append it to the list
        encoding = face_recognition.face_encodings(image)[0]
        encoded_list.append(encoding)
    return encoded_list

# Prepare a list of filenames from your photos directory
photo_filenames = ["p1.jpg", "p2.jpg", "p3.jpg", "p4.jpg"]
my_face_encodings = encode_faces(photo_filenames)

# Get a reference to the webcam
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(my_face_encodings, face_encoding)

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = f"Matched: Photo {photo_filenames[first_match_index]}"
        else:
            name = "Unknown"

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
