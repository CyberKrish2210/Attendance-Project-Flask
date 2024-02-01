import cv2
import face_recognition
import os

def detect_and_match_face(video_path, image_locations):
    # Load the video
    cap = cv2.VideoCapture(video_path)

    # Initialize face recognition
    known_face_encodings = []

    # Load images and encode faces from the list of image locations
    for image_location in image_locations:
        image = face_recognition.load_image_file(image_location)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face in the current frame
        for face_encoding in face_encodings:
            # Check if the face matches any known face
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # If a match is found, return the index of the first match
            if True in matches:
                first_match_index = matches.index(True)
                return first_match_index

    # Release the video capture
    cap.release()

    # If no face is found, return -1
    return -1

# Example usage
'''video_path = r'C:/Users/yashp/PycharmProjects/Face_Recognition_Flask/uploaded_video.mp4'
image_locations = ['C:/Users/yashp/PycharmProjects/Face_Recognition_Flask/images/Yash.jpeg', 'C:/Users/yashp/PycharmProjects/Face_Recognition_Flask/images/YashT.jpeg']
index = detect_and_match_face(video_path, image_locations)
print(f'It is {image_locations[index]}')

# Print the index value
print(f'Index of matched face: {index}')
'''