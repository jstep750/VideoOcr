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

def cal_time_to_frame(time, fps):
    frame_number = (time * fps)
    # fps는 flaot값으로 나오기 때문에 float값 상태에서 곱해준 뒤, 반올림을 해야 가장 근접한 프레임이 나온다.
    return round(frame_number)

if not os.path.exists('image_frames'):
    os.makedirs('image_frames')
 
#  create our video path
vidpath = os.path.join(os.getcwd(),'Downloads')
#test_vid = cv2.VideoCapture('testvideo.mp4')
test_vid = cv2.VideoCapture(os.path.join(vidpath,'kakaocoding.mp4'))

# start our index or count for  the frames
fps = int(test_vid.get(cv2.CAP_PROP_FPS))
print(fps)

width = (test_vid.get(cv2.CAP_PROP_FRAME_WIDTH))   
height  = (test_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))   

x = float(0.3477020317256139)
y = float(0.38044326517871074)
w = float(0.652297968274386)
h = float(0.5883408771656001)
start_time = 440
end_time = 540
start_frame_num = cal_time_to_frame(start_time, fps)
end_frame_num = cal_time_to_frame(end_time, fps)
print(start_frame_num, end_frame_num)

index = 0
while test_vid.isOpened():
    ret,frame = test_vid.read()
    frame = frame[int(height*y): int(height*(y + h)), int(width*x): int(width*(x + w))]
    if not ret:
        break

    if(index>start_frame_num and index<end_frame_num):
        #assign a name for our files 
        name = './image_frames/frame' + str(int(index)) + '.png'
        
        #assign our print statement
        print ('Extracting frames...' + name)
        cv2.imwrite(name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    index = index + 1
    
test_vid.release()
cv2.destroyAllWindows()  # destroy all the opened windows
