import re
import json

def parse_with_boxes(filepath):
    items = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\[\[([\d.]+),\s*([\d.]+)\],\s*\[([\d.]+),\s*([\d.]+)\],\s*\[([\d.]+),\s*([\d.]+)\],\s*\[([\d.]+),\s*([\d.]+)\]\]:\s*(.*?)\s*\((.*?)\)", line.strip())
            if m:
                x1, y1 = float(m.group(1)), float(m.group(2))
                x3, y3 = float(m.group(5)), float(m.group(6))
                text = m.group(9)
                score = float(m.group(10))
                items.append({'box': (x1, y1, x3, y3), 'text': text, 'score': score})
    return items

items3 = parse_with_boxes("debug_logs/ocr_page_3.txt")
items4 = parse_with_boxes("debug_logs/ocr_page_4.txt")

def split_tiers(items):
    right_page = [it for it in items if it['box'][0] >= 1074]
    left_page = [it for it in items if it['box'][0] < 1074]
    return right_page, left_page

p8, p9 = split_tiers(items3)
p10, p11 = split_tiers(items4)

print(f"P8: {len(p8)}, P9: {len(p9)}, P10: {len(p10)}, P11: {len(p11)}")

with open("debug_logs/pages_analysis.txt", "w", encoding="utf-8") as f:
    for name, page_items in [('P8', p8), ('P9', p9), ('P10', p10), ('P11', p11)]:
        f.write(f"\n==============================\n=== {name} (items: {len(page_items)}) ===\n==============================\n")
        if not page_items:
            continue
        ys = [it['box'][1] for it in page_items]
        f.write(f"Y-range: {min(ys):.1f} to {max(ys):.1f}\n")
        for tier_idx, (y_start, y_end) in enumerate([(100, 360), (360, 640), (640, 920), (920, 1200), (1200, 1500)], 1):
            tier_items = [it for it in page_items if y_start <= it['box'][1] < y_end]
            tier_items_sorted = sorted(tier_items, key=lambda it: -it['box'][0])
            f.write(f"\n--- {name} Tier {tier_idx} (y: {y_start}-{y_end}, count: {len(tier_items)}) ---\n")
            texts = [it['text'] for it in tier_items_sorted]
            f.write(" ".join(texts) + "\n")

print("Done parsing tiers")
