# -*- coding: utf-8 -*-
import json

with open("debug_logs/xinhua_idioms.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

lines = []
for it in dict_data[:50]:
    drv = it.get('derivation', '')
    if drv and drv != '无':
        lines.append(f"{it['word']}: {drv}")

with open("debug_logs/sample_derivations.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Wrote 50 sample derivations.")
