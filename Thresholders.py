import cv2

image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_borders/Highway_2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
cv2.imshow("Original", image)
cv2.imshow("Binary", thresh)
cv2.waitKey(0)