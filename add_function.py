import cv2

image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_borders/Highway_2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 127, 255)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
addition = cv2.add(canny, thresh)
cv2.imshow("Adition", addition)
cv2.waitKey(0)