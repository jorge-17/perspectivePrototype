import cv2
import numpy as np


def getMatrix(frame):
    cv2.circle(frame, (269, 489), 5, (255, 255, 0), -1)
    cv2.circle(frame, (542, 1078), 5, (255, 60, 0), -1)
    cv2.circle(frame, (1779, 921), 5, (0, 255, 6), -1)
    cv2.circle(frame, (558, 463), 5, (0, 0, 255), -1)

    pts1 = np.float32([[269, 489], [558, 463], [542, 1078], [1779, 921]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return matrix

def getPerspectiveView(frame, matrix):    
    result = cv2.warpPerspective(frame, matrix, (500, 600))
    return result

def TansformPoint(matrix, point):
    original = np.array([(( point[0], point[1]))], dtype=np.float32)
    original = np.array([original])
    converted = cv2.perspectiveTransform(original, matrix)
    return converted

