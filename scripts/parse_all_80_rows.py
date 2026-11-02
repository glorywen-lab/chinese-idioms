import json
import re

with open("debug_logs/full_pdf_ocr.json", "r", encoding="utf-8") as f:
    all_ocr = json.load(f)

# PDF structure:
# Page 0 (PDF 1): Right = Printed P.4 (Rows 1-5), Left = Printed P.5 (Rows 6-10)
# Page 1 (PDF 2): Right = Printed P.6 (Rows 11-15), Left = Printed P.7 (Rows 16-20)
# Page 2 (PDF 3): Right = Printed P.8 (Rows 21-25), Left = Printed P.9 (Rows 26-30)
# Page 3 (PDF 4): Right = Printed P.10 (Rows 31-35), Left = Printed P.11 (Rows 36-40)
# Page 4 (PDF 5): Right = Printed P.12 (Rows 41-45), Left = Printed P.13 (Rows 46-50)
# Page 5 (PDF 6): Right = Printed P.14 (Rows 51-55), Left = Printed P.15 (Rows 56-60)
# Page 6 (PDF 7): Right = Printed P.16 (Rows 61-65), Left = Printed P.17 (Rows 66-70)
# Page 7 (PDF 8): Right = Printed P.18 (Rows 71-75), Left = Printed P.19 (Rows 76-80)

tier_y_ranges = [
    (100, 360),
    (360, 640),
    (640, 920),
    (920, 1200),
    (1200, 1520)
]

all_rows = {}
row_counter = 1

for pno in range(8):
    items = all_ocr[str(pno)]
    # In each PDF spread, width is ~2148. Middle line is around 1074.
    # Right page is x >= 1074 (printed page 2*pno + 4)
    # Left page is x < 1074 (printed page 2*pno + 5)
    right_items = [it for it in items if it['box'][0][0] >= 1074]
    left_items = [it for it in items if it['box'][0][0] < 1074]
    
    for page_items, page_num in [(right_items, 2*pno + 4), (left_items, 2*pno + 5)]:
        for tier_idx, (y_start, y_end) in enumerate(tier_y_ranges, 1):
            tier_items = [it for it in page_items if y_start <= it['box'][0][1] < y_end]
            # Chinese columns read right to left (-x)
            sorted_items = sorted(tier_items, key=lambda it: -it['box'][0][0])
            
            # Clean items: remove numbers (page numbers), stroke tags like 【一 畫】, '筆畫索引'
            cleaned_texts = []
            for it in sorted_items:
                t = it['text'].strip()
                # filter out numbers like '123', '【...】', '筆畫索引', '筆畫', '索引'
                if re.match(r'^\d+$', t): continue
                if '筆畫' in t or '索引' in t: continue
                if re.match(r'^【.*?】$', t): continue
                if len(t) < 2: continue
                cleaned_texts.append(t)
                
            all_rows[row_counter] = {
                'row_id': row_counter,
                'printed_page': page_num,
                'tier_in_page': tier_idx,
                'items': cleaned_texts
            }
            row_counter += 1

print(f"Total rows parsed: {len(all_rows)}")
with open("debug_logs/parsed_80_rows_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=2)

# Print summary of first 10 rows and last 10 rows
for r in [1, 2, 3, 4, 28, 29, 30, 31, 32, 68, 69, 70, 79, 80]:
    if r in all_rows:
        row = all_rows[r]
        print(f"Row {r:02d} (P.{row['printed_page']} T{row['tier_in_page']}): {len(row['items'])} items -> {' '.join(row['items'][:5])} ...")
