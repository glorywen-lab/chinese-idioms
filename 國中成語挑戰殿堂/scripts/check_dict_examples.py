# -*- coding: utf-8 -*-
import json
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

dict_data = json.load(open("debug_logs/xinhua_idioms.json", encoding="utf-8"))
dict_map = {it['word']: it for it in dict_data}

db = json.load(open("debug_logs/full_all_units_database.json", encoding="utf-8"))

total_idioms = 0
found_in_dict = 0
has_real_example = 0
has_derivation = 0

for u_id, u in db.items():
    for it in u['idioms']:
        total_idioms += 1
        w = it['idiom']
        w_s = t2s.convert(w)
        entry = dict_map.get(w_s) or dict_map.get(w)
        if entry:
            found_in_dict += 1
            ex = entry.get('example', '')
            if ex and ex != '无' and ex != '無':
                has_real_example += 1
            drv = entry.get('derivation', '')
            if drv and drv != '无' and drv != '無':
                has_derivation += 1

print(f"Total idioms in our DB: {total_idioms}")
print(f"Found in Xinhua dict: {found_in_dict} ({found_in_dict/total_idioms*100:.1f}%)")
print(f"Has real example in dict: {has_real_example} ({has_real_example/total_idioms*100:.1f}%)")
print(f"Has derivation in dict: {has_derivation} ({has_derivation/total_idioms*100:.1f}%)")
