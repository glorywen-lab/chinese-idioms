import cv2

img = cv2.imread("debug_logs/tier_29.png")
# x is around 869, width of column is ~45 px
# Let's crop x from 840 to 900
col = img[:, 840:900]
cv2.imwrite("debug_logs/tier_29_col_870.png", col)
print("Saved column around x=870")
