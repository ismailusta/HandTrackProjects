import cv2
import os
import numpy as np
import time
import handTrackingModul as Htm

folderPath = "Header"
headerList = os.listdir(folderPath)
print(headerList)
overlayList = []

for imPath in headerList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
frameCanvas = np.zeros((720, 1280, 3), np.uint8)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = Htm.handDetector(minDetection=0.85)
drawColor = (255, 0, 255)
paintThick = 5
colorThick = 12
eraserThick = 100
xp, yp = 0, 0
while True:
    # 1.Import image
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not success:
        break
    # 2.Find Hand Landmarks
    frame = detector.findHands(frame, draw=False)
    lmList = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        xp, yp = 0, 0
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # 3.Check which fingers are up
        fingers = detector.fingersUp()
        # 4.If Selection Mode - Two finger are up
        if fingers[1] and fingers[2]:
            # Checking for the Click
            if y1 < 122:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
                    paintThick = 4
            cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), drawColor, paintThick, cv2.FILLED)
        # 5.If Drawing Mode - Index finger are up
        if fingers[1] and fingers[2] == False:
            cv2.circle(frame, (x1, y1), 5, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThick)
                cv2.line(frameCanvas, (xp, yp), (x1, y1), drawColor, eraserThick)
            else:
                cv2.line(frame,(xp, yp), (x1, y1), drawColor, colorThick)
                cv2.line(frameCanvas, (xp, yp), (x1, y1), drawColor, colorThick)
            xp, yp = x1, y1

    frameGray = cv2.cvtColor(frameCanvas, cv2.COLOR_BGR2GRAY)
    _, frameInv = cv2.threshold(frameGray, 50, 255, cv2.THRESH_BINARY_INV)
    frameInv = cv2.cvtColor(frameInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, frameInv)
    frame = cv2.bitwise_or(frame, frameCanvas)

    frame[0:122, 0:1280] = header
    cv2.imshow("Image", frame)
    cv2.imshow("Canvas", frameCanvas)
    quitKey = cv2.waitKey(1)
    if quitKey == 27:
        break
cap.release()
cv2.destroyAllWindows()
