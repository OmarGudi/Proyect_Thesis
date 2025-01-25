import cv2

#convert first to black and grey image
image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_borders/Highway_2.jpg', 0)
output = cv2.Canny(image, 100, 500)
cv2.imshow("Original", image)
cv2.imshow("Detection", output)
cv2.waitKey(0)
