import cv2
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
img = cv2.imread("debug_logs/tier_29_col_870.png")
# upscale 2x
img_up = cv2.resize(img, (0,0), fx=3, fy=3)
res, _ = ocr(img_up)
for r in res:
    print(r[1])
