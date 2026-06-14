import cv2
import numpy as np

# 1. Initialize the default webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Solve mirroring: rotate 180 degrees horizontally (flip around y-axis)
    frame = cv2.flip(frame, 1)

    # Get original dimensions
    height, width = frame.shape[:2]
    
    # 2. Downscale to exactly half height and width for the base of our grid
    half_h, half_w = height // 2, width // 2
    small_frame = cv2.resize(frame, (half_w, half_h))

    # --- 3. Create the four quadrants ---

    # Top-Left: Original feed (downscaled)
    top_left = small_frame.copy()

    # Top-Right: Flipped vertically
    top_right = cv2.flip(small_frame, 0)

    # Bottom-Left: Feed in HSV
    bottom_left = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)

    # Bottom-Right: Pure Red channel only
    # Note: OpenCV uses BGR, so Red is index 2. 
    # We create a 3-channel image where Blue and Green are zeros.
    red_channel = small_frame[:, :, 2]
    bottom_right = np.zeros_like(small_frame)
    bottom_right[:, :, 2] = red_channel

    # --- Assemble the final window ---
    # Stack Top rows and Bottom rows horizontally, then stack them vertically
    top_row = np.hstack((top_left, top_right))
    bottom_row = np.hstack((bottom_left, bottom_right))
    final_output = np.vstack((top_row, bottom_row))

    # Display the result
    cv2.imshow('System Feed', final_output)

    # Break loop on 'e' key press
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()