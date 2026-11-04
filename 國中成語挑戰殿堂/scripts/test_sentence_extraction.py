# -*- coding: utf-8 -*-
import json
import re
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

dict_data = json.load(open("debug_logs/xinhua_idioms.json", encoding="utf-8"))
dict_map = {it['word']: it for it in dict_data}

db = json.load(open("debug_logs/full_all_units_database.json", encoding="utf-8"))

def extract_clean_example(ex_raw, idiom):
    if not ex_raw or ex_raw in ["无", "無"]:
        return None
    ex_t = s2t.convert(ex_raw)
    # Remove ★《...》
    cleaned = re.sub(r'★.*', '', ex_t).strip()
    cleaned = re.sub(r'《.*?》.*', '', cleaned).strip()
    if not cleaned or len(cleaned) < 6:
        return None
    if '～' in cleaned:
        return cleaned.replace('～', '【　　】')
    elif idiom in cleaned:
        return cleaned.replace(idiom, '【　　】')
    return None

def extract_clean_derivation(drv_raw, idiom):
    if not drv_raw or drv_raw in ["无", "無"]:
        return None
    drv_t = s2t.convert(drv_raw)
    # find book title
    m = re.search(r'(《.*?》)(.*)', drv_t)
    if m:
        book = m.group(1)
        quote = m.group(2).strip(' “"”：:，,')
        if len(quote) > 8:
            if idiom in quote:
                return f"{book}典籍名句：「{quote.replace(idiom, '【　　】')}」"
            else:
                # If idiom not directly in quote, can be phrased as:
                # e.g. 《淮南子》：「見一葉落而知歲之將暮。」後世便以【　　】比喻...
                return None
    return None

# Let's count how many idioms get valid sentences from this
ex_count = 0
drv_count = 0

for u_id, u in db.items():
    if u_id == "7_1_1": continue # already 100% handcrafted
    for it in u['idioms']:
        w = it['idiom']
        w_s = t2s.convert(w)
        entry = dict_map.get(w_s) or dict_map.get(w)
        if entry:
            ex_s = extract_clean_example(entry.get('example', ''), w)
            if ex_s: ex_count += 1
            drv_s = extract_clean_derivation(entry.get('derivation', ''), w)
            if drv_s: drv_count += 1

print(f"Total other idioms: {1435 - 78} = 1357")
print(f"Extracted clean examples: {ex_count}")
print(f"Extracted clean derivations with idiom: {drv_count}")
