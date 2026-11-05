# -*- coding: utf-8 -*-
import json
import os

with open(os.path.join(os.path.dirname(__file__), "..", "data", "full_all_units_database.json"), "r", encoding="utf-8") as f:
    db = json.load(f)

lines = []
for uid, u in db.items():
    uname = u.get("name", uid)
    for item in u["idioms"]:
        w = item["idiom"]
        for s_idx, s in enumerate(item["sentences"], 1):
            if "《" in s and "「" in s and "【　　】" in s:
                lines.append(f"[{uname}][{w}][變式{s_idx}] {s}")

with open(os.path.join(os.path.dirname(__file__), "..", "all_book_quotes_sentences.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Written {len(lines)} sentences to all_book_quotes_sentences.txt")
