# -*- coding: utf-8 -*-
import json
import re
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

with open("debug_logs/xinhua_idioms.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

dict_map = {it['word']: it for it in dict_data}

with open("debug_logs/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

def clean_example(ex_raw, idiom):
    if not ex_raw or ex_raw in ["无", "無"]:
        return None
    ex_t = s2t.convert(ex_raw)
    # 移除 ★ 標記及其後引書
    ex_t = re.sub(r'★.*', '', ex_t).strip()
    # 移除句尾 《...》
    ex_t = re.sub(r'《.*?》.*', '', ex_t).strip()
    if len(ex_t) < 8:
        return None
    if '～' in ex_t:
        return ex_t.replace('～', '【　　】')
    if idiom in ex_t:
        return ex_t.replace(idiom, '【　　】')
    return None

def clean_derivation(drv_raw, idiom):
    if not drv_raw or drv_raw in ["无", "無"]:
        return None
    drv_t = s2t.convert(drv_raw)
    # 典籍引用格式例如：《漢書·藝文志》：「...」
    m = re.search(r'(《[^》]+》[^\s：“"」]*)[：:「“"]+(.+?)[」”]', drv_t)
    if m:
        book = m.group(1).strip()
        quote = m.group(2).strip()
        if len(quote) >= 6:
            if idiom in quote:
                return f"{book}典籍名句：「{quote.replace(idiom, '【　　】')}」"
            else:
                return f"{book}載有名言：「{quote}」，後人常以【　　】來比喻此等情境。"
    return None

results = {}
for u_id, u in db.items():
    results[u_id] = {
        "name": u["name"],
        "total": len(u["idioms"]),
        "has_example": 0,
        "has_derivation": 0
    }
    for it in u["idioms"]:
        w = it["idiom"]
        w_s = t2s.convert(w)
        entry = dict_map.get(w_s) or dict_map.get(w)
        if entry:
            ex = clean_example(entry.get("example"), w)
            if ex:
                results[u_id]["has_example"] += 1
            drv = clean_derivation(entry.get("derivation"), w)
            if drv:
                results[u_id]["has_derivation"] += 1

with open("debug_logs/dict_coverage_report.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Coverage report written to debug_logs/dict_coverage_report.json")
