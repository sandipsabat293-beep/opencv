import cv2
import numpy as np
import os

possible_paths = ['img2.png', os.path.join('image', 'img2.png')]
img = None
for image_path in possible_paths:
    if os.path.exists(image_path):
        img = cv2.imread(image_path)
        if img is not None:
            print(f"Loaded image from: {image_path}")
            break

if img is None:
    print("Error: Image 'img2.png' not found in root or image/ directory.")
    exit()

h, w, c = img.shape
if w > 800:
    img = cv2.resize(img, (600, int(h * (600 / w))))

# Split the different color channels of the image
b, g, r = cv2.split(img)

zeros = np.zeros_like(b)

blue_channel_vis = cv2.merge([b, zeros, zeros])   # Pure Blue image
green_channel_vis = cv2.merge([zeros, g, zeros]) # Pure Green image
red_channel_vis = cv2.merge([zeros, zeros, r])   # Pure Red image

# Remove the Green channel and merge the remaining channels
merged_no_green = cv2.merge([b, zeros, r])

# Save all images
cv2.imwrite("channel_blue.png", blue_channel_vis)
cv2.imwrite("channel_green.png", green_channel_vis)
cv2.imwrite("channel_red.png", red_channel_vis)
cv2.imwrite("merged_no_green.png", merged_no_green)
print("All channel images and the merged image have been saved!")

cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Blue Channel", cv2.WINDOW_NORMAL)
cv2.namedWindow("Green Channel", cv2.WINDOW_NORMAL)
cv2.namedWindow("Red Channel", cv2.WINDOW_NORMAL)
cv2.namedWindow("Merged (No Green Channel)", cv2.WINDOW_NORMAL)

# Uniform size
cv2.resizeWindow("Original Image", 400, 300)
cv2.resizeWindow("Blue Channel", 400, 300)
cv2.resizeWindow("Green Channel", 400, 300)
cv2.resizeWindow("Red Channel", 400, 300)
cv2.resizeWindow("Merged (No Green Channel)", 400, 300)

# Show images
cv2.imshow("Original Image", img)
cv2.imshow("Blue Channel", blue_channel_vis)
cv2.imshow("Green Channel", green_channel_vis)
cv2.imshow("Red Channel", red_channel_vis)
cv2.imshow("Merged (No Green Channel)", merged_no_green)

print("Click on any window and press any key to close.")
cv2.waitKey(0)
cv2.destroyAllWindows()