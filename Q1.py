import cv2
import numpy as np
import os

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions
from mediapipe.tasks.python.vision.core import image as mp_image
from mediapipe.tasks.python.core import base_options as base_options_lib

MODEL_PATH = "hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print(f"Model file not found: {MODEL_PATH}")
    print("Download the MediaPipe hand_landmarker task model and place it in the script directory, or update MODEL_PATH to the correct location.")
    exit(1)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

canvas = np.zeros((480, 640, 3), dtype=np.uint8)
prev_x, prev_y = None, None

hand_options = HandLandmarkerOptions(
    base_options=base_options_lib.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

hands = HandLandmarker.create_from_options(hand_options)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_input = mp_image.Image(mp_image.ImageFormat.SRGB, rgb)

    result = hands.detect(mp_input)

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]
        h, w, _ = frame.shape
        landmark = hand[8]
        x = int(landmark.x * w)
        y = int(landmark.y * h)

        if prev_x is not None:
            cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 255, 0), 5)

        prev_x, prev_y = x, y
    else:
        prev_x, prev_y = None, None

    output = cv2.add(frame, canvas)
    cv2.imshow("Virtual Drawing Board", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.imwrite("drawing.png", canvas)
        print("Drawing Saved")
    elif key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()



