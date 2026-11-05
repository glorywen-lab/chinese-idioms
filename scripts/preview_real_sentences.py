# -*- coding: utf-8 -*-
import json

with open("debug_logs/extracted_real_sentences.json", "r", encoding="utf-8") as f:
    extracted = json.load(f)

lines = []
count = 0
for uid in ['7_1_2', '7_2_1', '8_1_1', '9_1_1']:
    items = extracted[uid]
    for it in items[:5]:
        lines.append(f"Unit: {uid} | Idiom: {it['idiom']}")
        lines.append(f"  Exp: {it['explanation']}")
        lines.append(f"  Ex : {it['example']}")
        lines.append(f"  Drv: {it['derivation']}")
        lines.append("-" * 40)

with open("debug_logs/sample_real_sentences_preview.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Wrote sample preview.")
