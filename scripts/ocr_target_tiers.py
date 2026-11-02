from rapidocr_onnxruntime import RapidOCR
import cv2

ocr = RapidOCR()

with open("debug_logs/tier_ocr_results.txt", "w", encoding="utf-8") as out:
    for tier in [29, 30, 31, 32]:
        img = cv2.imread(f"debug_logs/tier_{tier}.png")
        result, _ = ocr(img)
        # In Chinese dictionary, text is arranged in vertical columns reading right-to-left.
        # But OCR might return text segments. Let's record bbox and text.
        sorted_items = sorted(result, key=lambda x: (-x[0][0][0], x[0][0][1]))
        out.write(f"\n=== TIER {tier} ===\n")
        for item in sorted_items:
            bbox, text, conf = item
            out.write(f"[{bbox[0][0]:.0f}, {bbox[0][1]:.0f}] {text} ({conf:.2f})\n")

print("OCR results written to debug_logs/tier_ocr_results.txt")
