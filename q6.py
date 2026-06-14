import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam is not opening.")
    exit()

kernel_size = 5

print("--- Controls ---")
print("Press 'w' : Increase blur (Softer Edges)")
print("Press 's' : Decrease blur (Sharper Edges)")
print("Press 'e' : Exit the program\n")


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    frame = cv2.flip(frame, 1)

    # Convert the feed to Grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur dynamically using 'kernel_size'
    blurred_frame = cv2.GaussianBlur(gray_frame, (kernel_size, kernel_size), 0)

    # Pass the blurred image through a Canny Edge Detector
    edges = cv2.Canny(blurred_frame, 100, 200)

    status_text = f"Kernel Size: {kernel_size}x{kernel_size}"
    cv2.putText(edges, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Real-time Canny Edge Detector", edges)

    key = cv2.waitKey(1) & 0xFF

    # press 'w' to increase blur 
    if key == ord('w'):
        kernel_size += 2
        print(f"Blur increased! New Kernel Size: {kernel_size}")

    # press 's' to decrease blur
    elif key == ord('s'):
        if kernel_size > 1:
            kernel_size -= 2
            print(f"Blur decreased! New Kernel Size: {kernel_size}")

    # Press 'e' to exit loop
    elif key == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()