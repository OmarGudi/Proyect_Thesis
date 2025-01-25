import cv2

image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_borders/Highway_2.jpg')
cv2.imshow('Original', image)
original_image = image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 100, 255)
contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 255, 0),1)
cv2.imshow('Contours', image)
cv2.imshow('Canny', canny)
cv2.waitKey(0)