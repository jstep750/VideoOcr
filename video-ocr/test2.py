import pytesseract
from pytesseract import Output
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import os
# import fastwer
import sys
# codec error 해결
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


# get grayscale image

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,3)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation 팽창 (글씨가 더 팽창)
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion 침식 (글씨가 더 얇아짐)
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation ( 침식 후 팽창)
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def closing(image): #팽창 후 침식
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)  

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction 기울시 수정
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

def resize(image):
    size = (7016, 4961)
    image = cv2.resize(image,  dsize=size, interpolation=cv2.INTER_LINEAR)
    return image
    
def img_Contrast(img): 
    #-----Converting image to LAB Color model----------------------------------- 
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB) 
    # -----Splitting the LAB image to different channels------------------------- 
    l, a, b = cv2.split(lab) 
    # -----Applying CLAHE to L-channel------------------------------------------- 
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)) 
    cl = clahe.apply(l) 
    # -----Merge the CLAHE enhanced L-channel with the a and b channel----------- 
    limg = cv2.merge((cl, a, b)) 
    # -----Converting image from LAB Color model to RGB model-------------------- 
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR) 
    return final
def blur(img):
    return cv2.bilateralFilter(img, 5, 75, 75)


def ocr(image, lang): # ocr
    custom_config = r'-c preserve_interword_spaces=1 --oem 3 --psm 6 -l ' + lang
    d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
    df = pd.DataFrame(d)
    result_text = ''
    # clean up blanks
    df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
    # sort blocks vertically
    sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
    for block in sorted_blocks:
        curr = df1[df1['block_num']==block]
        sel = curr[curr.text.str.len()>3]
        char_w = (sel.width/sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = 0, 0, 0
        text = ''
        for ix, ln in curr.iterrows():
            # add new line when necessary
            if prev_par != ln['par_num']:
                text += '\n'
                prev_par = ln['par_num']
                prev_line = ln['line_num']
                prev_left = 0
            elif prev_line != ln['line_num']:
                text += '\n'
                prev_line = ln['line_num']
                prev_left = 0

            added = 0  # num of spaces that should be added
            if ln['left']/char_w > prev_left + 1:
                added = int((ln['left'])/char_w) - prev_left
                text += ' ' * added 
            text += ln['text'] + ' '
            prev_left += len(ln['text']) + added + 1
        text += '\n'
        # print(text)
        result_text += text
    return result_text


def blur_and_gray(image): # blur + gray
    return get_grayscale(blur(image))

def blur_gray_threshold(image):
    return thresholding(blur_and_gray(image))

def opening_b_g_th(image):
    return opening(blur_gray_threshold(image))

def closing_b_g_th(image):
    return closing(blur_gray_threshold(image))


# 이미지를 받아서 ocr후 텍스트 반환
if __name__ == '__main__':

    string = ''

    for i in range(0,8):
        input = './image_frame11/frame' + str(i) + '.png'
        img = cv2.imread(input) # 이미지 불러오고
        img = resize(img)
        img = closing_b_g_th(img)
        result = ocr(img, 'eng')
        #print(result, end='')
        br = '\n-------------------------------'+str(i)+'-----------------------------------\n'
        string = string + br + result
        print(result+br)

    print(string)
