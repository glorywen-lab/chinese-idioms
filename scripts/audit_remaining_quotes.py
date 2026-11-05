# -*- coding: utf-8 -*-
import json

quotes = json.load(open("quotes_to_fix.json", encoding="utf-8"))
print(f"Total remaining quotes with blank: {len(quotes)}")

# 看看是否有包含現代口氣、或是多餘詞彙的
suspect_words = ["因此", "所以", "如果", "但是", "那麼", "這就是", "正是", "所謂", "也就是", "換言之", "由此可見", "足見", "因而"]
flagged_remaining = []

for q in quotes:
    text = q["quote"]
    for sw in suspect_words:
        if sw in text:
            flagged_remaining.append((q, sw))
            break

print(f"Flagged remaining with modern connectives inside quote: {len(flagged_remaining)}")
for f, sw in flagged_remaining:
    print(f"[{f['uid']}][{f['idiom']}] 現代詞 '{sw}': 「{f['quote']}」")
    print(f"  原句: {f['full']}")
