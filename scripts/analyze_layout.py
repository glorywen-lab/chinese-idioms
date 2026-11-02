import fitz
import cv2
import numpy as np
import os

pdf_path = r"G:\其他電腦\我的電腦\GloryCloud\01_教學\0-教學資料\參考資料\成語典.pdf"
doc = fitz.open(pdf_path)

output_log = []
output_log.append(f"Total PDF pages: {len(doc)}")

for page_idx in range(len(doc)):
    page = doc[page_idx]
    pix = page.get_pixmap(dpi=150)
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    if pix.n == 4:
        img_data = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        img_data = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    # Detect horizontal lines
    # Binary threshold
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (img_data.shape[1] // 10, 1))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Sum across rows to find horizontal line positions
    row_sums = np.sum(horizontal, axis=1)
    line_indices = np.where(row_sums > img_data.shape[1] * 0.2 * 255)[0]
    
    # Group continuous lines
    grouped_lines = []
    if len(line_indices) > 0:
        current_group = [line_indices[0]]
        for idx in line_indices[1:]:
            if idx == current_group[-1] + 1:
                current_group.append(idx)
            else:
                grouped_lines.append(int(np.mean(current_group)))
                current_group = [idx]
        grouped_lines.append(int(np.mean(current_group)))
        
    output_log.append(f"Page {page_idx + 1}: height={pix.height}, width={pix.width}, horizontal lines at y={grouped_lines}")

with open("debug_logs/layout_analysis.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_log))
print("Layout analysis written to debug_logs/layout_analysis.txt")
