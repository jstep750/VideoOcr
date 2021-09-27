#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Wed Nov 28 12:33:08 2018

@author: jordansauchuk
'''


import os
import cv2
#conda install -c conda-forge opencv  
#https://anaconda.org/conda-forge/opencv

#create our directory for the frames

if not os.path.exists('image_frames'):
    os.makedirs('image_frames')
 
#  create our video path
vidpath = os.path.join(os.getcwd(),'Downloads')
#test_vid = cv2.VideoCapture('testvideo.mp4')
test_vid = cv2.VideoCapture(os.path.join(vidpath,'e9273173533245009d2a6adc2700b32e.mp4'))

# start our index or count for  the frames

index = 0
while test_vid.isOpened():
    ret,frame = test_vid.read()
    if not ret:
        break

    if(index%100 == 0):
        #assign a name for our files 
        name = './image_frames/frame' + str(int(index/100)) + '.png'
        
        #assign our print statement
        print ('Extracting frames...' + name)
        cv2.imwrite(name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    index = index + 1
    
test_vid.release()
cv2.destroyAllWindows()  # destroy all the opened windows
