# -*- coding: utf-8 -*-
import json

with open("quotes_to_fix.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

for q in quotes:
    if q["uid"] == "8_2_1":
        print(f"[{q['idiom']}][變式{q['variant']}] 《{q['book']}》: 「{q['quote']}」")
