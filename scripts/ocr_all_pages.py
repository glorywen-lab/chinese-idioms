import fitz
from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np
import json
import time

ocr = RapidOCR()
pdf_path = r"G:\其他電腦\我的電腦\GloryCloud\01_教學\0-教學資料\參考資料\成語典.pdf"
doc = fitz.open(pdf_path)

print(f"Total PDF pages: {len(doc)}")
all_ocr_results = {}

t0 = time.time()
for pno in range(len(doc)):
    page = doc[pno]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    result, _ = ocr(img)
    # Convert result to serializable
    items = []
    if result:
        for r in result:
            bbox, text, conf = r
            items.append({
                'box': bbox,
                'text': text,
                'conf': float(conf)
            })
    all_ocr_results[pno] = items
    print(f"Page {pno+1} OCR done: {len(items)} items ({time.time()-t0:.1f}s)")

with open("debug_logs/full_pdf_ocr.json", "w", encoding="utf-8") as f:
    json.dump(all_ocr_results, f, ensure_ascii=False)

print(f"All 8 pages OCR completed in {time.time()-t0:.1f}s, saved to debug_logs/full_pdf_ocr.json")
