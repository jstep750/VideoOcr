from PIL import Image
import pytesseract
import argparse
import cv2
import os
 

# load the example image and convert it to grayscale
image = cv2.imread(r"C:\Users\jstep\prev-workspaces\VideoOcr\video-ocr\image_frames\4e9309a735fa4978b492a35f3b54f4d7\frame5.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = r"C:\Users\jstep\prev-workspaces\VideoOcr\video-ocr\image_frames\4e9309a735fa4978b492a35f3b54f4d7\frame55.png"
cv2.imwrite(filename, gray)

#pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

text = pytesseract.image_to_string(Image.open(filename))

print(text)