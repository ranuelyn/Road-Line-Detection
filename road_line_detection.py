# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 03:12:54 2023

@author: yusuf
"""

import cv2
import numpy as np

def drawLines(image, lines):
    image = np.copy(image)
    blankImg = np.zeros((image.shape[0], image.shape[1], 3), dtype = np.uint8)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blankImg, (x1, y1), (x2, y2), (0, 255, 0), thickness = 3)

    image = cv2.addWeighted(image, 0.9, blankImg, 1, 0)
    return image

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    imgMasked = cv2.bitwise_and(image, mask)
    
    return imgMasked
    

def process(image):
    height, width = img.shape[0], img.shape[1]
    
    #region_of_interest_vertices = [(0, height), (width / 2, height / 2),(width, height)]
    region_of_interest_vertices = [(0, height), (width / 2, height / 2), (width, height / 1.5),(width, height)]

     
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 250, 120)
    
    imgCropped = region_of_interest(imgCanny, np.array([region_of_interest_vertices], np.int32))
    lines = cv2.HoughLinesP(imgCropped, rho = 2, theta = np.pi / 180, threshold = 220, lines = np.array([]), minLineLength = 150, maxLineGap = 5)
    #print(lines)
    
    imgWithLine = drawLines(image, lines)
    
    return imgWithLine


cap = cv2.VideoCapture('video1.mp4')

while True:
    success, img = cap.read()
    img = process(img)
    
    
    if success:
        cv2.imshow('RLD', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()