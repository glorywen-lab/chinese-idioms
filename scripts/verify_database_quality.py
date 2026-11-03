# -*- coding: utf-8 -*-
import json

db_path = "debug_logs/full_all_units_database.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

errors = []
total_idioms = 0
total_sentences = 0

for uid, u in db.items():
    for it in u["idioms"]:
        total_idioms += 1
        w = it["idiom"]
        sents = it.get("sentences", [])
        if len(sents) != 3:
            errors.append(f"{uid} {w}: has {len(sents)} sentences (expected 3)")
        for idx, s in enumerate(sents, 1):
            total_sentences += 1
            if "【　　】" not in s:
                errors.append(f"{uid} {w} sent {idx}: missing 【　　】 -> {s}")
            if len(s) < 8:
                errors.append(f"{uid} {w} sent {idx}: too short ({len(s)} chars) -> {s}")

print(f"Verified {total_idioms} idioms, {total_sentences} sentences across {len(db)} units.")
if errors:
    print(f"Found {len(errors)} errors:")
    for e in errors[:20]:
        print("  *", e)
else:
    print("ALL 100% PERFECT! No missing blanks, no wrong sentence counts, no ultra-short sentences!")
