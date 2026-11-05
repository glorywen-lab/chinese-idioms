# -*- coding: utf-8 -*-
import json

with open("data/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

u = db["8_1_1"]

lines = []
lines.append(f"單元：{u.get('name', '8_1_1')}（共 {len(u['idioms'])} 則成語）")
lines.append("=" * 60)
lines.append("待答題 (變式一·經典文學) 逐題檢視：\n")

for i, item in enumerate(u["idioms"], 1):
    idiom = item["idiom"]
    meaning = item.get("meaning", "")
    s1 = item["sentences"][0] if item["sentences"] else "無句子"
    lines.append(f"{i:2d}. 【{idiom}】")
    lines.append(f"    釋義：{meaning}")
    lines.append(f"    變式一：{s1}\n")

with open("inspect_8_1_1_variant1.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Saved to inspect_8_1_1_variant1.txt successfully!")
