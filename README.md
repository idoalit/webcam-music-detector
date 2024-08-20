# Webcam Music Detector

## Description

This Python application utilizes a webcam to detect the presence of people and plays music when a person is detected. The music continues to play in a loop as long as a person is present in the frame. Once no person is detected, the music stops. The application also features functionality to dynamically handle file paths and manage virtual environments.

## Features

- Real-time person detection using OpenCV.
- Music playback controlled by Pygame.
- Dynamic handling of script paths with batch and shell scripts.
- Virtual environment support for isolated package management.

## Requirements

- Python 3.x
- OpenCV
- Pygame
- Ultralytics YOLOv8

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/idoalit/webcam-music-detector.git
   ```
2. Navigate to the project directory:
   ```sh
   cd webcam-music-detector
   ```
3. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```sh
   python music.py
   ```
   
   or use Yolo instead

   ```sh
   python yolo.py
   ```
2. To stop the running script, use the provided `stop.bat` file.

## Batch Files

- `start.bat`: Activates the virtual environment and runs the Python script.
- `stop.bat`: Closes any running Python scripts.