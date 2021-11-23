import cv2

src0 = cv2.imread("./image_frame2/frame0.png")
src1 = cv2.imread("./image_frame2/frame1.png")

diff = cv2.absdiff(src0, src1)
cv2.imwrite('./image_frame4/framediff.png', diff)