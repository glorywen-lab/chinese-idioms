# -*- coding: utf-8 -*-
import json

with open("data/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for uid, u in db.items():
    if not isinstance(u, dict) or "idioms" not in u:
        continue
    for item in u["idioms"]:
        if "愧" in item["idiom"] or "怍" in item["idiom"]:
            print(f"Unit {uid}: {item['idiom']}")
