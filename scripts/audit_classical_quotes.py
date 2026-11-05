# -*- coding: utf-8 -*-
import json
import re
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "data", "full_all_units_database.json")
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

all_quotes_with_blank = []

for uid, u in db.items():
    uname = u.get("name", uid)
    for item in u["idioms"]:
        w = item["idiom"]
        for s_idx, s in enumerate(item["sentences"], 1):
            matches = re.findall(r"《([^》]+)》[^「]*[：:]*[「“]([^」”]+)[」”]", s)
            for book, q in matches:
                if "【　　】" in q:
                    all_quotes_with_blank.append({
                        "uid": uid,
                        "uname": uname,
                        "idiom": w,
                        "variant": s_idx,
                        "book": book,
                        "quote": q,
                        "full_sent": s
                    })

print(f"Total quotes with blank inside quotes: {len(all_quotes_with_blank)}")

# 分類統計有明顯偽造特徵的：
patterns = [
    r"是為【　　】",
    r"實為【　　】",
    r"可謂【　　】",
    r"堪稱【　　】",
    r"這正是【　　】",
    r"真可謂【　　】",
    r"此【　　】也",
    r"此【　　】之",
    r"乃【　　】之",
    r"何其【　　】",
    r"豈可【　　】",
    r"誠【　　】也",
    r"真【　　】也",
    r"真【　　】矣",
    r"必致【　　】",
    r"莫如【　　】",
    r"未免【　　】",
    r"此非【　　】",
    r"後世以【　　】",
    r"後衍為【　　】"
]

flagged = []
for item in all_quotes_with_blank:
    q = item["quote"]
    for pat in patterns:
        if re.search(pat, q):
            flagged.append((item, pat))
            break

print(f"Total flagged suspect quotes: {len(flagged)}")
with open(os.path.join(os.path.dirname(__file__), "..", "temp_flagged_quotes.json"), "w", encoding="utf-8") as f:
    json.dump([{"uid": x[0]["uid"], "idiom": x[0]["idiom"], "variant": x[0]["variant"], "book": x[0]["book"], "pat": x[1], "full": x[0]["full_sent"]} for x in flagged], f, ensure_ascii=False, indent=2)

for f_item, pat in flagged[:15]:
    print(f"[{f_item['uname']}][{f_item['idiom']}][變式{f_item['variant']}] 書名: 《{f_item['book']}》")
    print(f"  原句: {f_item['full_sent']}")
