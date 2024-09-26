import cv2
import numpy as np
import time
import handTrackingModul as Htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()  # -65=> 0 || 0=> 100 Volume Values
minVal, maxVal = volRange[0], volRange[1]
camWidth, camHeight = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, camWidth)  # 3 = cv2.CAP_PROP_FRAME_WIDTH
cap.set(4, camHeight)  # 4 = cv2.CAP_PROP_FRAME_HEIGHT
detector = Htm.handDetector(minDetection=0.7)
pTime = 0
vol = 0
volBar = 400
volPer = 0
while True:
    success, frame = cap.read()
    if not success:
        break
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, 0, False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2
        cv2.circle(frame, (x1, y1), 2, (0, 255, 0), 15, cv2.FONT_HERSHEY_PLAIN)
        cv2.circle(frame, (x2, y2), 2, (0, 255, 0), 15, cv2.FONT_HERSHEY_PLAIN)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2, cv2.FONT_HERSHEY_PLAIN)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), 15, cv2.FONT_HERSHEY_PLAIN)
        length = math.hypot(x2-x1, y2-y1)
        # Hand Range 20-260 || Volume Range -65-0
        vol = np.interp(length, [20, 260], [minVal, maxVal])
        volBar = np.interp(length, [20, 260], [400, 150])
        volPer = np.interp(length, [20, 260], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        if length < 20:
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), 15, cv2.FONT_HERSHEY_PLAIN)
            volume.GetMute()
        if length >= 260:
            cv2.circle(frame, (x1, y1), 2, (0, 0, 255), 15, cv2.FONT_HERSHEY_PLAIN)
            cv2.circle(frame, (x2, y2), 2, (0, 0, 255), 15, cv2.FONT_HERSHEY_PLAIN)
    cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(frame, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(frame, f'{int(volPer)}%', (40, 450), 1, 2, (255, 0, 0), 2, cv2.FONT_HERSHEY_PLAIN)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS:{int(fps)}', (10, 50), 1, 2, (255, 0, 0), 2, cv2.FONT_HERSHEY_PLAIN)
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC KEY
        break
cap.release()
cv2.destroyAllWindows()
