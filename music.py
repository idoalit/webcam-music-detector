import cv2
import pygame
import time

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")

# Set music volume (e.g., 0.5 for 50% volume)
initial_volume = 0.5
pygame.mixer.music.set_volume(initial_volume)

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
fade_out_duration = 10  # Duration of the fade-out effect in seconds
delay_seconds = 10  # Delay time before starting fade-out

def fade_out_music(start_volume, duration):
    """Smoothly fade out the music volume."""
    steps = 100  # Number of steps for the fade-out
    fade_step_duration = duration / steps
    for step in range(steps):
        volume = start_volume * (1 - step / steps)
        pygame.mixer.music.set_volume(volume)
        time.sleep(fade_step_duration)
    pygame.mixer.music.stop()

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
                fade_out_music(pygame.mixer.music.get_volume(), fade_out_duration)
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
