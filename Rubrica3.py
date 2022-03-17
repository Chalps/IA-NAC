import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture(1)
prevCircle = None
def dist(x1, y1, x2, y2): return (x1 - x2) ** 2 + (y1 - y2) ** 2


while True:
    videoCapture.set(3, 640)
    videoCapture.set(4, 480)
    ret, frame = videoCapture.read()
    if not ret:
        break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (5, 5), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT,
                              1, 20, param1=50, param2=30, minRadius=0, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None:
                chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i

        cv.circle(blurFrame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
        cv.circle(blurFrame, (chosen[0], chosen[1]),
                  chosen[2], (255, 100, 100), 3)
        prevCircle = chosen

    cv.imshow("circles", blurFrame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
