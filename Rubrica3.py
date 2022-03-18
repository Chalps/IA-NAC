import math
from re import I
from math import atan
import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture(1)
def dist(x1, y1, x2, y2): return (x1 - x2) ** 2 + (y1 - y2) ** 2


def slopeLine(x1, y1, x2, y2):
    return (float)(y2 - y1)/(x2 - x1)


def findAngle(m1, m2):
    tanAngle = abs((m2 - m1) / (1 + m1 * m2))
    angle = atan(tanAngle)
    angleDegrees = (angle * 180) / math.pi
    return round(angleDegrees, 2)


while True:
    videoCapture.set(3, 1640)
    videoCapture.set(4, 1480)
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

        if len(circles[0]) == 2:
            x1 = circles[0][0][0]
            y1 = circles[0][0][1]
            x2 = circles[0][1][0]
            y2 = circles[0][1][1]

            m1 = slopeLine(x1, y1, x2, y2)
            m2 = slopeLine(0, 375, 1200, 375)
            angle1 = findAngle(m1, m2)
            angle2 = 180 - angle1

            xString1 = str(angle1)
            xString2 = str(angle2)

            cv.putText(blurFrame, str('Angulos em relacao plano horizontal: '), (0, 350),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 200, 255), 2, cv.LINE_AA, False)
            cv.putText(blurFrame, str('Angulo 1: ' + xString1 + ' deg'), (0, 400),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA, False)
            cv.putText(blurFrame, str('Angulo 2: ' + xString2 + ' deg'), (0, 450),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA, False)

            cv.line(blurFrame, (x1, y1), (x2, y2),  (255, 100, 100), 8)

    cv.imshow("circles", blurFrame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
