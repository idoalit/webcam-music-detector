import cv2.dnn
import numpy as np
from ultralytics.utils import ASSETS, yaml_load
from ultralytics.utils.checks import check_yaml
import time
import pygame
import json

# Load configuration from a JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

CLASSES = yaml_load(check_yaml(config["coco_yaml"]))["names"]
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))

pygame.mixer.init()
pygame.mixer.music.load(config["music_file"])  # Specify your music file here

def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f"{CLASSES[class_id]} ({confidence:.2f})"
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def main():
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(config["onnx_model"])
    
    cap = cv2.VideoCapture(0)
    last_detection_time = time.time()
    music_playing = False

    while True:
        ret, original_image = cap.read()
        if not ret:
            break

        height, width, _ = original_image.shape
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image

        scale = length / 640
        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
        model.setInput(blob)

        outputs = model.forward()
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes, scores, class_ids = [], [], []
        person_detected = False

        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                    outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2],
                    outputs[0][i][3],
                ]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

                if CLASSES[maxClassIndex] == "person":
                    person_detected = True
                    last_detection_time = time.time()

        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            draw_bounding_box(
                original_image,
                class_ids[index],
                scores[index],
                round(box[0] * scale),
                round(box[1] * scale),
                round((box[0] + box[2]) * scale),
                round((box[1] + box[3]) * scale),
            )

        current_time = time.time()
        
        if person_detected:
            if not music_playing:
                pygame.mixer.music.play(-1)  # Loop indefinitely
                pygame.mixer.music.set_volume(1.0)
                music_playing = True
        else:
            if music_playing and (current_time - last_detection_time) > config["delay_seconds"]:
                for i in range(100, -1, -1):
                    pygame.mixer.music.set_volume(i / 100)
                    time.sleep(config["fade_out_duration"] / 100)
                pygame.mixer.music.stop()
                music_playing = False

        # Display the resulting frame if configured
        if config["display_frame"]:
            cv2.imshow("Webcam", original_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
