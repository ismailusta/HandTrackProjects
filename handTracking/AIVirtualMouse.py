import cv2
import numpy as np
import time
import handTrackingModul as Htm
import autopy
frameR = 100
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smothVal = 5
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = Htm.handDetector(maxHand=1)
wScreen, hScreen = autopy.screen.size()
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not success:
        break
    frame = detector.findHands(frame)
    lmList, bbox = detector.findPosition(frame, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(frame, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
        # Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))

            clocX = plocX + (x3 - plocX) / smothVal
            clocY = plocY + (y3 - plocY) / smothVal
            autopy.mouse.move(clocX, clocY)
            plocX, plocY = clocX, clocY

            cv2.circle(frame, (x1, y1), 4, (50, 205, 50), 20, cv2.FILLED)
        if fingers[1] == 1 and fingers[2] == 1:
            length, frame, infoLine = detector.findDistance(8, 12, frame)
            print(length)
            if length < 35:
                cv2.circle(frame, (infoLine[4], infoLine[5]), 4, (0, 0, 255), 15, cv2.FILLED)
                autopy.mouse.click()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS:{int(fps)}', (450, 50), 1, 2, (255, 0, 0), 2, cv2.FONT_HERSHEY_PLAIN)
    cv2.imshow("Image", frame)
    quit_Key = cv2.waitKey(1)
    if quit_Key == 27:
        break
cap.release()
cv2.destroyAllWindows()