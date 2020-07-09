import tensorflow as tf
import posenet
import cv2


def getPoints(cap):
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    image, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    orig = image.copy()

    for contour in contours:        
        x, y, w, h = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 1000:
            continue

        #subframe = cv2.resize(frame2[y:y+h,x:x+w], (224,224), interpolation = cv2.INTER_AREA)
        #os.chdir(r'C:\Users\jrodarte\posenetPory\pedestrian\imgBank')
        #cv2.imwrite('img'+str(time())+'.jpg',subframe)

        color1 = (0, 255, 0)
        if w/h > 0.7:
            color1 = (0, 0, 255)
            continue
        else:
            return x, y, w, h
        

        #print(w, h)
        
    frame1 = frame2
    ret, frame2 = cap.read()
    #return (ptTobillos_x, ptTobillos_y)
