import math
from re import I
import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture(1)
def dist(x1, y1, x2, y2): return (x1 - x2) ** 2 + (y1 - y2) ** 2


while True:
    videoCapture.set(3, 640)
    videoCapture.set(4, 480)
    ret, frame = videoCapture.read()
    if not ret:
        break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (9, 9), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT,
                              1, 20, param1=50, param2=30, minRadius=80, maxRadius=90)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(blurFrame, (i[0], i[1]), i[2], (255, 100, 100), 3)
            cv.circle(blurFrame, (i[0], i[1]), 2, (255, 0, 0), 3)

    cv.imshow("circles", blurFrame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
