import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 100)

def RIO(image):
    height = image.shape[0]
    polygons = np.array([[(310, 225), (390, 225), (390, height), (310, height)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

while True:
    control, frame = cap.read()
    if not control:
        print("Error: Failed to capture frame")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 130, 150)
    _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
    thresh = RIO(thresh)
    if thresh is None:
        print("Error: RIO returned None for thresh")
        break
    final = cv2.add(canny, thresh)
    region_of_interest = RIO(final)
    if region_of_interest is None:
        print("Error: RIO returned None for final")
        break
    contours, _ = cv2.findContours(region_of_interest, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        print(area)
        if 900 <= area <= 2800:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            print(cx, cy)
            if 130 <= cx <= 160:
                cv2.putText(frame, "Forward", (15, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            elif 160 <= cx <= 190:
                cv2.putText(frame, "Right", (15, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            elif 90 <= cx <= 130:
                cv2.putText(frame, "Left", (15, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.circle(frame, ((50 + 240) // 2, (240 + 240) // 2), 5, (255, 0, 0), -1)
            cv2.line(frame, (cx, cy), ((50 + 240) // 2, (240 + 240) // 2), (0, 0, 255), 2)
    cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
    cv2.imshow("Threshold", thresh)
    cv2.imshow("CSI camera", frame)
    cv2.imshow("Edge Detection", canny)
    cv2.imshow("ROI Detection", region_of_interest)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
