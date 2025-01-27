import cv2
import numpy as np

image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_borders/Highway_example.jpg')
roi = image[300:400, 50:200]
cv2.imshow('ROI', roi)
cv2.imshow('Original', image)
cv2.waitKey(0)