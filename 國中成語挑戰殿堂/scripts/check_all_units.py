import json
import re
import opencc

s2t = opencc.OpenCC('s2t')

with open("debug_logs/cleaned_80_rows.json", "r", encoding="utf-8") as f:
    all_rows = json.load(f)

# Load existing 8上2段 questions (100 idioms, 300 sentences)
with open("debug_logs/questions_multi_8_2.json", "r", encoding="utf-8") as f:
    existing_8_2 = json.load(f)

existing_8_2_map = {it['idiom']: it for it in existing_8_2}

# Define 20 Units
unit_definitions = [
    {"id": "7_1_1", "name": "7上 第1次段考", "grade": "7年級", "rows": [1, 2, 3, 4]},
    {"id": "7_1_2", "name": "7上 第2次段考", "grade": "7年級", "rows": [5, 6, 7, 8]},
    {"id": "7_1_3", "name": "7上 第3次段考", "grade": "7年級", "rows": [9, 10, 11, 12]},
    {"id": "7_2_1", "name": "7下 第1次段考", "grade": "7年級", "rows": [13, 14, 15, 16]},
    {"id": "7_2_2", "name": "7下 第2次段考", "grade": "7年級", "rows": [17, 18, 19, 20]},
    {"id": "7_2_3", "name": "7下 第3次段考", "grade": "7年級", "rows": [21, 22, 23, 24]},
    {"id": "8_1_1", "name": "8上 第1次段考", "grade": "8年級", "rows": [25, 26, 27, 28]},
    {"id": "8_1_2", "name": "8上 第2次段考", "grade": "8年級", "rows": [29, 30, 31, 32]},
    {"id": "8_1_3", "name": "8上 第3次段考", "grade": "8年級", "rows": [33, 34, 35, 36]},
    {"id": "8_2_1", "name": "8下 第1次段考", "grade": "8年級", "rows": [37, 38, 39, 40]},
    {"id": "8_2_2", "name": "8下 第2次段考", "grade": "8年級", "rows": [41, 42, 43, 44]},
    {"id": "8_2_3", "name": "8下 第3次段考", "grade": "8年級", "rows": [45, 46, 47, 48]},
    {"id": "9_1_1", "name": "9上 第1次段考", "grade": "9年級", "rows": [49, 50, 51, 52]},
    {"id": "9_1_2", "name": "9上 第2次段考", "grade": "9年級", "rows": [53, 54, 55, 56]},
    {"id": "9_1_3", "name": "9上 第3次段考", "grade": "9年級", "rows": [57, 58, 59, 60]},
    {"id": "9_2_1", "name": "9下 第1次段考", "grade": "9年級", "rows": [61, 62, 63, 64]},
    {"id": "9_2_2", "name": "9下 第2次段考", "grade": "9年級", "rows": [65, 66, 67, 68]},
    {"id": "extra_1", "name": "其實還有 · 拔尖卷(一)", "grade": "進階擴充", "rows": [69, 70, 71, 72]},
    {"id": "extra_2", "name": "其實還有 · 拔尖卷(二)", "grade": "進階擴充", "rows": [73, 74, 75, 76]},
    {"id": "extra_3", "name": "其實還有 · 終極卷(三)", "grade": "進階擴充", "rows": [77, 78, 79, 80]}
]

total_idioms_count = 0
for u in unit_definitions:
    u_idioms = []
    for r in u['rows']:
        r_str = str(r)
        if r_str in all_rows:
            u_idioms.extend([it['idiom'] for it in all_rows[r_str]['idioms']])
    total_idioms_count += len(u_idioms)
    print(f"[{u['grade']}] {u['name']}: {len(u_idioms)} 成語 (Rows {u['rows'][0]}~{u['rows'][-1]})")

print(f"\nTotal idioms across all 20 units: {total_idioms_count}")
