import cv2
import numpy as np
import os
import time

possible_paths = ["img.png", os.path.join("image", "img.png")]
img = None
for path in possible_paths:
    if os.path.exists(path):
        img = cv2.imread(path)
        if img is not None:
            print(f"Loaded image from: {path}")
            break

if img is None:
    raise FileNotFoundError(
        "Could not load img.png. Place the file in the script folder or in the image/ directory."
    )

start = time.time()

denoised = cv2.fastNlMeansDenoisingColored(
    img, None, 15, 15, 7, 21
)

end = time.time()

h, w, c = img.shape

print("Width :", w)
print("Height:", h)
print("Channels:", c)
print("Total Pixels:", w*h)
print("Processing Time:", round(end-start,3), "seconds")

cv2.imwrite("clean_output.png", denoised)

cv2.imshow("Original", img)
cv2.imshow("Denoised", denoised)

cv2.waitKey(0)
cv2.destroyAllWindows()