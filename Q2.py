import cv2
import time

# Initialize webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Checking if the webcam opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

prev_frame_time = 0
new_frame_time = 0
img_counter = 0

print("Controls:")
print("Press 'c' to capture and save the image")
print("Press 'x' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    #Live FPS Calculation
    new_frame_time = time.time()
    # formula: FPS = 1 / (current_frame_time - previous_frame_time)
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    
    # Convert FPS to integer for clean display
    fps_text = f"FPS: {int(fps)}"
    # Display FPS on the Live Feed
    # cv2.putText(image, text, org, font, fontScale, color, thickness)
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Webcam Live Feed', frame)

    key = cv2.waitKey(1) & 0xFF

    #Save Image when key 'c' is pressed
    if key == ord('c'):
        img_name = f"captured_frame_{img_counter}.png"
        cv2.imwrite(img_name, frame)
        print(f"Successfully saved {img_name}!")
        img_counter += 1

    # Press 'x' to exit the loop
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()