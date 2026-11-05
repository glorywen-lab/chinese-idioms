# -*- coding: utf-8 -*-
import json
import re
import os

with open(os.path.join(os.path.dirname(__file__), "..", "data", "full_all_units_database.json"), "r", encoding="utf-8") as f:
    db = json.load(f)

for uid, u in db.items():
    uname = u.get("name", uid)
    count = 0
    quotes_list = []
    for item in u["idioms"]:
        w = item["idiom"]
        for s_idx, s in enumerate(item["sentences"], 1):
            m = re.search(r"《([^》]+)》[^「]*[：:]*[「“]([^」”]*【　　】[^」”]*)[」”]", s)
            if m:
                count += 1
                quotes_list.append((w, s_idx, m.group(1), m.group(2), s))
    print(f"{uid:10s} ({uname:15s}): {count} 句引號內挖空")
