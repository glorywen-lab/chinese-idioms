import fitz
import cv2
import numpy as np

doc = fitz.open(r"G:\其他電腦\我的電腦\GloryCloud\01_教學\0-教學資料\參考資料\成語典.pdf")

# Page 3 (0-indexed: 2) -> P9 is Left half (x < width/2)
# Page 4 (0-indexed: 3) -> P10 is Right half (x >= width/2)

p3 = doc[2].get_pixmap(dpi=200)
p4 = doc[3].get_pixmap(dpi=200)

img3 = np.frombuffer(p3.samples, dtype=np.uint8).reshape((p3.height, p3.width, p3.n))
img4 = np.frombuffer(p4.samples, dtype=np.uint8).reshape((p4.height, p4.width, p4.n))

if p3.n == 4: img3 = cv2.cvtColor(img3, cv2.COLOR_RGBA2BGR)
if p4.n == 4: img4 = cv2.cvtColor(img4, cv2.COLOR_RGBA2BGR)

# Dimensions at 200 dpi
h3, w3 = img3.shape[:2]
h4, w4 = img4.shape[:2]

# P9 is left half of img3: x from 0 to w3//2
# Row 29 is Tier 4 of P9: y from ~ 0.60 * h3 to 0.79 * h3
# Row 30 is Tier 5 of P9: y from ~ 0.79 * h3 to 0.98 * h3
# P10 is right half of img4: x from w4//2 to w4
# Row 31 is Tier 1 of P10: y from ~ 0.08 * h4 to 0.26 * h4
# Row 32 is Tier 2 of P10: y from ~ 0.26 * h4 to 0.44 * h4

cv2.imwrite("debug_logs/tier_29.png", img3[int(0.60*h3):int(0.80*h3), :w3//2])
cv2.imwrite("debug_logs/tier_30.png", img3[int(0.79*h3):int(0.98*h3), :w3//2])
cv2.imwrite("debug_logs/tier_31.png", img4[int(0.08*h4):int(0.27*h4), w4//2:])
cv2.imwrite("debug_logs/tier_32.png", img4[int(0.26*h4):int(0.45*h4), w4//2:])

print("Saved tier images to debug_logs/")
