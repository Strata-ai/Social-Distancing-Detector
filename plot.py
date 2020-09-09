#!/usr/bin/env python

'''
Contain functions to draw Bird Eye View for region of interest(ROI) and draw bounding boxes according to risk factor
for humans in a frame and draw lines between boxes according to risk factor between two humans. 
'''

__title__           = "plot.py"
__Version__         = "1.0"
__copyright__       = "Copyright 2020 , Social Distancing AI"
__license__         = "MIT"
__author__          = "Deepak Birla"
__email__           = "birla.deepak26@gmail.com"
__date__            = "2020/05/29"
__python_version__  = "3.5.2"

# imports
import cv2
import numpy as np


# Function to draw bounding boxes according to risk factor for humans in a frame and draw lines between
# boxes according to risk factor between two humans.
# Red: High Risk
# Yellow: Low Risk
# Green: No Risk 
def social_distancing_view(frame, distances_mat, boxes, risk_count):
    
    high_risk_color = (255, 0, 0)
    safe_color = (0, 255, 0)
    low_risk_color = (255, 255, 0)
    background_color = (150, 150, 150)
    
    for i in range(len(boxes)):

        x,y,w,h = boxes[i][:]
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),safe_color,2)
                           
    for i in range(len(distances_mat)):

        per1 = distances_mat[i][0]
        per2 = distances_mat[i][1]
        closeness = distances_mat[i][2]
        
        if closeness == 1:
            x,y,w,h = per1[:]
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),low_risk_color,2)
                
            x1,y1,w1,h1 = per2[:]
            frame = cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),low_risk_color,2)
                
            frame = cv2.line(frame, (int(x+w/2), int(y+h/2)), (int(x1+w1/2), int(y1+h1/2)),low_risk_color, 2)
            
    for i in range(len(distances_mat)):

        per1 = distances_mat[i][0]
        per2 = distances_mat[i][1]
        closeness = distances_mat[i][2]
        
        if closeness == 0:
            x,y,w,h = per1[:]
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),high_risk_color,2)
                
            x1,y1,w1,h1 = per2[:]
            frame = cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),high_risk_color,2)
                
            frame = cv2.line(frame, (int(x+w/2), int(y+h/2)), (int(x1+w1/2), int(y1+h1/2)),high_risk_color, 2)
            
    pad = np.full((50,frame.shape[1],3), background_color, dtype=np.uint8)
    cv2.putText(pad, "HIGH RISK : " + str(risk_count[0]) + " people", (50, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, high_risk_color, 1)
    cv2.putText(pad, "LOW RISK : " + str(risk_count[1]) + " people", (350, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, low_risk_color, 1)
    cv2.putText(pad, "SAFE : " + str(risk_count[2]) + " people", (650,  30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, safe_color, 1)
    frame = np.vstack((frame,pad))
            
    return frame


def detection_view(image, boxes):
    
    green = (0, 255, 0)

    
    for i in range(len(boxes)):

        x,y,w,h = boxes[i][:]
        image = cv2.rectangle(image,(x,y),(x+w,y+h),green,2)
                           
    return image
