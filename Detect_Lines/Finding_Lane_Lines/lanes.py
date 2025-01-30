import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slop_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return left_line, right_line

def canny(image):
    global gray, blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Set a filter to the image
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    #Canny function or method to identy fy the edges
    canny = cv2.Canny(blur, 50, 150)
    #Showing results
    #cv2.imshow('Image', gray)
    #cv2.imshow('Image with filter', blur)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 50, 0), 10)
    return line_image

#Region of interest
def ROI(image):
    height = image.shape[0]
    polygons = np.array([
        [(250, height), (1100, height), (550, 250)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

'''
#This is to be used with an image
#Convert out example image to gray scale using opencv
image = cv2.imread(r'/home/omargudino/Documents/Proyect_Thesis/Detect_Lines/Finding_Lane_Lines/test_image.jpg')
lane_image = np.copy(image)
canny_image = canny(image)
cropped_image = ROI(canny_image)
lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
average_lines = average_slop_intercept(lane_image, lines)
line_image = display_lines(lane_image, average_lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
#Showing results
cv2.imshow('Line Image', combo_image)
cv2.waitKey(0)
'''

#This is to be used with a video
cap = cv2.VideoCapture(r'/home/omargudino/Documents/Proyect_Thesis/Detect_Lines/Finding_Lane_Lines/test2.mp4')
while((cap.isOpened())):
    _, frame =  cap.read()
    canny_image = canny(frame)
    cropped_image = ROI(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    average_lines = average_slop_intercept(frame, lines)
    line_image = display_lines(frame, average_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    #Showing results
    cv2.imshow('Line Image', combo_image)
    if cv2.waitKey(10) == ord('e'):
        break
cap.release()
cv2.destroyAllWindows()
#plt.imshow(canny)
#plt.show()

