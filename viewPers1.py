import cv2
import numpy as np
import tensorflow as tf
import posenet
import perspective
import time
import mqtt_pub as publish

cap = cv2.VideoCapture('vtest4.mp4')
#img donde se acumulan los puntos
acum_image = np.zeros((600, 500), dtype=np.uint8)
tiempo_ult_frame=time.time()
while True:
    
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    diff = cv2.absdiff(frame1, frame2)
    matrix = perspective.getMatrix(frame1)
    #vista pajaro
    result = perspective.getPerspectiveView(frame1, matrix)

    # black blank image
    blank_image = np.zeros((600, 500), dtype=np.uint8)
    

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    image, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    orig = image.copy()
    
    for contour in contours:        
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 1000:
            continue        

        color1 = (0, 255, 0)
        if w/h > 0.7:
            color1 = (0, 0, 255)
        else:
            #if(h > 80 and w > 40):
            puntoTobillo = [int((x+w)-(w/2)),(y+h)]
            puntoTobilloTrans = perspective.TansformPoint(matrix, puntoTobillo)
            #cv2.circle(frame1, (int((x+w)-(w/2)),(y+h)), 3, (0, 0, 255), -1)
            
            cv2.circle(blank_image,(puntoTobilloTrans[0][0][0], puntoTobilloTrans[0][0][1]), 15, (255,255,255), -1)
            cv2.circle(result,(puntoTobilloTrans[0][0][0], puntoTobilloTrans[0][0][1]), 15, (255,255,255), -1)
            
            #Info frame
            #cv2.rectangle(frame1, (x, y), (x+w, y+h), color1, 2)
            #cv2.putText(frame1, "(w={},h={})".format(w,h), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            #cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)            """            
            
            #cv2.imshow("feed2", orig)
        #print(w, h)
    # Generacion del heat map        
    threshold = 4
    maxValue = 2
    ret, th1 = cv2.threshold(blank_image, threshold, maxValue, cv2.THRESH_BINARY)

    # add to the accumulated image
    acum_image = cv2.add(acum_image, th1*3)
    color_image_video = cv2.applyColorMap(acum_image, cv2.COLORMAP_HOT)
    frameImageProm = color_image_video.mean()*10    
    
    cv2.putText(color_image_video, "Prom: {}".format(frameImageProm), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    if time.time()-tiempo_ult_frame > 1:
        acum_image = acum_image.clip(min=1)
        acum_image = acum_image - 1
        tiempo_ult_frame=time.time()
    #print(type(frameImageProm))
    publish.publishData(frameImageProm)

    #cv2.imshow("Frame", frame1)
    #cv2.imshow("Perspective transformation", result)
    #cv2.imshow("Vista pajaro", acum_image)
    cv2.imshow("Black window", color_image_video)    

    key = cv2.waitKey(1)
    if key == 27 & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
