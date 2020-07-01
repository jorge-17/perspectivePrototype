import cv2
import numpy as np
import tensorflow as tf
import posenet
import perspective as pes
import points as po

cap = cv2.VideoCapture('vtest2.mp4')

while True:
    _, frame = cap.read()
    result = pes.getPerspectiveView(frame)
    puntoTobillo = po.getPoints(cap)
    #print(puntoTobillo)
    #cv2.circle(frame, (int(ptTobillos_x), int(ptTobillos_y)), 5, (0, 0, 0), -1)
    cv2.imshow("Frame", frame)
    cv2.imshow("Perspective transformation", result)

    key = cv2.waitKey(1)
    if key == 27 & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
