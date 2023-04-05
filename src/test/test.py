import cv2
import numpy as np

# # Load image
# img = cv2.imread("src/images/cat.jpg")

# # Load the cascade
# face_cascade = cv2.CascadeClassifier('src/test/haarcascade_frontalcatface.xml')


# # Convert into grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Detect faces
# faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# # Draw a rectangle around the faces and remove them from the image
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), -1)

# # Display the output
# cv2.imshow('output', img)
# cv2.waitKey()