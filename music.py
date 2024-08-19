import cv2
import pygame
import time

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")

# Set music volume (e.g., 0.5 for 50% volume)
pygame.mixer.music.set_volume(0.5)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Function to detect if a person is in the frame
def person_detected(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Return True if faces are detected, otherwise False
    return len(faces) > 0

# Variables to control music playback
music_playing = False
last_person_detected_time = None
delay_seconds = 20  # Delay time before stopping the music

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if a person is detected
    if person_detected(frame):
        if not music_playing:
            pygame.mixer.music.play(-1)  # Play music in a loop
            music_playing = True
        # Update the last person detected time
        last_person_detected_time = time.time()
    else:
        if music_playing:
            if last_person_detected_time is not None and (time.time() - last_person_detected_time) >= delay_seconds:
                pygame.mixer.music.stop()  # Stop the music
                music_playing = False
    
    # Display the resulting frame (optional)
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Small delay to reduce CPU usage
    time.sleep(0.1)

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
