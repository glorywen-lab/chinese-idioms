# -*- coding: utf-8 -*-
import json
import sys

unit_id = sys.argv[1] if len(sys.argv) > 1 else "8_2_1"

with open("data/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

u = db[unit_id]
print(f"單元代碼: {unit_id}")
print(f"單元名稱: {u.get('name', unit_id)}")
print(f"成語總數: {len(u['idioms'])}")
print("-" * 50)
for i, item in enumerate(u['idioms'], 1):
    w = item['idiom']
    meaning = item.get('meaning', '')
    sents = item.get('sentences', [])
    s_preview = sents[0] if sents else '無'
    print(f"{i:2d}. {w}: {s_preview[:30]}...")
