import cv2
import numpy as np


def getPerspectiveView(frame):
    cv2.circle(frame, (645, 227), 5, (0, 0, 255), -1)
    cv2.circle(frame, (4, 721), 5, (0, 0, 255), -1)
    cv2.circle(frame, (1282, 721), 5, (0, 0, 255), -1)
    cv2.circle(frame, (1167, 237), 5, (0, 0, 255), -1)

    pts1 = np.float32([[645, 227], [1167, 237], [4, 721], [1282, 721]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))
    return result