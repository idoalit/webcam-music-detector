import cv2
import pygame
import time
import json

# Load configuration from file
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load(config["music_file"])

# Set initial music volume
initial_volume = config["initial_volume"]
pygame.mixer.music.set_volume(initial_volume)

# Initialize the webcam with the configured camera index
cap = cv2.VideoCapture(config["camera_index"])

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces and draw boundaries
def detect_and_draw_faces(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), tuple(config["rectangle_color"]), config["rectangle_thickness"])
    
    # Return True if faces are detected, otherwise False
    return len(faces) > 0

# Variables to control music playback
music_playing = False
last_person_detected_time = None
fade_out_duration = config["fade_out_duration"]
delay_seconds = config["delay_seconds"]

def fade_out_music(start_volume, duration):
    """Smoothly fade out the music volume."""
    steps = 100  # Number of steps for the fade-out
    fade_step_duration = duration / steps
    for step in range(steps):
        volume = start_volume * (1 - step / steps)
        pygame.mixer.music.set_volume(volume)
        time.sleep(fade_step_duration)
    pygame.mixer.music.stop()

def play_music():
    """Play music with initial volume."""
    pygame.mixer.music.set_volume(initial_volume)
    pygame.mixer.music.play(-1)  # Play music in a loop

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Detect faces and draw boundaries
    if detect_and_draw_faces(frame):
        if not music_playing:
            play_music()
            music_playing = True
        # Update the last person detected time
        last_person_detected_time = time.time()
    else:
        if music_playing:
            if last_person_detected_time is not None and (time.time() - last_person_detected_time) >= delay_seconds:
                fade_out_music(pygame.mixer.music.get_volume(), fade_out_duration)
                music_playing = False
    
    # Display the resulting frame if configured
    if config["display_frame"]:
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
