# -*- coding: utf-8 -*-
import json
import re
import os

with open(os.path.join(os.path.dirname(__file__), "..", "data", "full_all_units_database.json"), "r", encoding="utf-8") as f:
    db = json.load(f)

# 找出所有包含《書名》且有引號「...」的句子
all_book_quotes = []

for uid, u in db.items():
    uname = u.get("name", uid)
    for item in u["idioms"]:
        w = item["idiom"]
        for s_idx, s in enumerate(item["sentences"], 1):
            # 尋找 《...》...「...」
            m = re.findall(r"《([^》]+)》[^「]*[：:]*[「“]([^」”]+)[」”]", s)
            for book, q in m:
                all_book_quotes.append({
                    "uid": uid,
                    "uname": uname,
                    "idiom": w,
                    "variant": s_idx,
                    "book": book,
                    "quote": q,
                    "blank_in_quote": "【　　】" in q,
                    "full": s
                })

print(f"Total book quotes: {len(all_book_quotes)}")
blank_in_quotes = [x for x in all_book_quotes if x["blank_in_quote"]]
print(f"Blank in quotes: {len(blank_in_quotes)}")

# 匯出所有 blank_in_quotes 供精準檢修
with open(os.path.join(os.path.dirname(__file__), "..", "quotes_to_fix.json"), "w", encoding="utf-8") as f:
    json.dump(blank_in_quotes, f, ensure_ascii=False, indent=2)

print("Exported quotes_to_fix.json successfully!")
