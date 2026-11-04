# -*- coding: utf-8 -*-
import json
import re
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

dict_data = json.load(open("debug_logs/xinhua_idioms.json", encoding="utf-8"))
dict_map = {it['word']: it for it in dict_data}

# Test sample idioms across various units
test_words = ["一暴十寒", "一葉知秋", "八仙過海", "狡兔三窟", "望梅止渴", "背水一戰", "臥薪嚐膽", "畫蛇添足", "守株待兔", "掩耳盜鈴"]

for w in test_words:
    w_s = t2s.convert(w)
    entry = dict_map.get(w_s) or dict_map.get(w)
    if entry:
        print(f"=== {w} ===")
        print("釋義:", s2t.convert(entry.get('explanation', '')))
        print("例句:", s2t.convert(entry.get('example', '')))
        print("典故:", s2t.convert(entry.get('derivation', ''))[:80])
