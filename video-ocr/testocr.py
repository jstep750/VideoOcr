#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Wed Nov 28 12:33:08 2018

@author: jordansauchuk
'''

from PIL import Image
import pytesseract
from wand.image import Image as Img
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import numpy as np
import cv2

img = cv2.imread("./image_frame9/frame0.png")
height, width, channels = img.shape
print(img.shape)

string = ''

print("hello")

#width = (video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))   
#height  = (video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))   

for i in range(0,8):
    frame = './image_frame11/frame' + str(i) + '.png'
    demo = Image.open(frame)
    #demo = np.array(demo)
    #demo = demo[int(height*y): int(height*(y + h)), int(width*x): int(width*(x + w))]
    text = pytesseract.image_to_string(demo, lang = 'eng')
    br = '\n-------------------------------'+str(i)+'-----------------------------------\n'
    string = string + br + text
    print(text+br)

print(string)


















