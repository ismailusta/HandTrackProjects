import cv2
import time
import os
import handTrackingModul as Htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)

filePath = "FingerImages"
fingerList = os.listdir(filePath)
overlayList = []
for i in fingerList:
    imageResized = cv2.resize(cv2.imread(f'{filePath}/{i}'), (200, 200))
    overlayList.append(imageResized)
pTime = 0
trendLandMark = [4, 8, 12, 16, 20]
detector = Htm.handDetector(minDetection=0.8)
while True:
    success, frame = cap.read()
    if not success:
        break
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    frame[0:200, 0:200] = overlayList[0]
    if len(lmList) != 0:
        fingers = []
        if lmList[trendLandMark[0]][1] > lmList[trendLandMark[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for i in range(1, 5):
            if lmList[trendLandMark[i]][2] < lmList[trendLandMark[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
        h, w, c = overlayList[totalFingers-1].shape
        frame[0:h, 0:w] = overlayList[totalFingers-1]
        cv2.rectangle(frame, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(totalFingers), (65, 355), 5, 4, (255, 0, 0), 10, cv2.FONT_HERSHEY_PLAIN)
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS:{int(fps)}', (450, 50), 1, 2, (255, 0, 0), 2, cv2.FONT_HERSHEY_PLAIN)
    cv2.imshow("Image", frame)
    quit_Key = cv2.waitKey(1)

    if quit_Key == 27:
        break
cap.release()
cv2.destroyAllWindows()
