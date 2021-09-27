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


string = ''

for i in range(10,20):
    frame = './image_frames/frame' + str(i) + '.png'
    demo = Image.open(frame)
    text = pytesseract.image_to_string(demo, lang = 'eng')
    string = string + text

print(string)


















