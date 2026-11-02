import fitz
from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np

ocr = RapidOCR()
doc = fitz.open(r"G:\其他電腦\我的電腦\GloryCloud\01_教學\0-教學資料\參考資料\成語典.pdf")

# Let's inspect page 3 and page 4 (where 8上2段 is located)
# Specifically, let's check Page 3 (printed pages 8 and 9) and Page 4 (printed pages 10 and 11)
for pno in [2, 3]: # 0-indexed: page 3 is idx 2, page 4 is idx 3
    page = doc[pno]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
    result, _ = ocr(img)
    with open(f"debug_logs/ocr_page_{pno+1}.txt", "w", encoding="utf-8") as f:
        if result:
            for item in result:
                bbox, text, score = item
                f.write(f"{bbox}: {text} ({score:.2f})\n")
    print(f"Page {pno+1} OCR finished, total items: {len(result) if result else 0}")
