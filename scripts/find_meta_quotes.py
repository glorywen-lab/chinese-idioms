# -*- coding: utf-8 -*-
import json
import re

with open("quotes_to_fix.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# 檢測引號內的結尾或接續特徵
# 凡是引號內有以下特徵的，都是把引申詞塞進引號裡的：
suffix_patterns = [
    r"[，,、\s]*(?:後世|後人|遂|故|此|是|蓋|真|實|可|未|人|世)*(?:遂以|遂演為|遂稱|遂成|引申為|演為|故稱|故以|是為|實為|可謂|堪稱|這正是|此之謂|此【　　】|真可謂|成千古|成【　　】|為【　　】之喻|之喻|之後世)[^」”]*$",
    r"[，,、\s]*(?:後世|後人|遂|故)*(?:以|常以|遂以|亦作)【　　】[^」”]*$"
]

matched = []
for q in quotes:
    text = q["quote"]
    # 檢查是否含有引申句
    has_meta = False
    for p in ["遂以", "遂演為", "遂稱", "遂成", "引申為", "演為", "故稱", "故以", "是為", "實為", "可謂", "堪稱", "這正是", "此之謂", "此【　　】", "真可謂", "成【　　】", "為【　　】之", "【　　】之喻", "後遂以", "後世遂以", "何其【　　】", "豈可【　　】"]:
        if p in text:
            has_meta = True
            break
    if has_meta:
        matched.append((q, p))

print(f"Total quotes with meta-text inside quotation marks: {len(matched)}")
for m, p in matched[:20]:
    print(f"[{m['uname']}][{m['idiom']}] (關鍵詞: {p})")
    print(f"  原句: {m['full']}")
