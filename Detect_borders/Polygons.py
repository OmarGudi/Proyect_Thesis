import cv2
import numpy as np

def RIO(image):
    height = image.shape[0]
    polygons = np.array([[(310, 225), (390, 225), (390, height), (310, height)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_borders/Highway_example.jpg') 
final = RIO(image)
cv2.imshow("Original", image)
cv2.imshow("Masked Image", final)
cv2.waitKey(0)          