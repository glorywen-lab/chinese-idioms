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

def get_real_example(entry, idiom_t, idiom_s):
    ex = entry.get('example', '')
    if not ex or ex in ['无', '無']:
        return None
    ex_t = s2t.convert(ex)
    # clean source
    ex_clean = re.sub(r'★.*', '', ex_t).strip()
    ex_clean = re.sub(r'《.*?》.*', '', ex_clean).strip()
    ex_clean = re.sub(r'（.*?）.*', '', ex_clean).strip()
    if len(ex_clean) < 8:
        return None
    if '～' in ex_clean:
        return ex_clean.replace('～', '【　　】')
    if idiom_t in ex_clean:
        return ex_clean.replace(idiom_t, '【　　】')
    if idiom_s in ex_clean:
        return ex_clean.replace(idiom_s, '【　　】')
    return None

def get_real_derivation(entry, idiom_t, idiom_s):
    drv = entry.get('derivation', '')
    if not drv or drv in ['无', '無']:
        return None
    drv_t = s2t.convert(drv)
    # Check if there is an explicit quote
    # Examples:
    # 语出《法华经·法师功德品》下至阿鼻地狱。”
    # 《论语·八佾》子曰‘《关雎》乐而不淫，哀而不伤。’”
    # 明·冯梦龙《醒世恒言》...
    m = re.search(r'([《〈][^》〉]+[》〉][^：:「“"”]*)[：:「“"\s]*(.+?)[」”"]', drv_t)
    if m:
        src = m.group(1).strip()
        quote = m.group(2).strip()
        if len(quote) >= 6:
            if idiom_t in quote:
                return f"{src}：「{quote.replace(idiom_t, '【　　】')}」"
            elif idiom_s in quote:
                return f"{src}：「{quote.replace(idiom_s, '【　　】')}」"
            else:
                return f"{src}名言：「{quote}」，後世多以【　　】比喻相類情境。"
    # If no quotes matched, check if book and idiom present
    m_book = re.search(r'([《〈][^》〉]+[》〉])', drv_t)
    if m_book and (idiom_t in drv_t or idiom_s in drv_t):
        book = m_book.group(1)
        # extract sentence containing idiom
        sents = re.split(r'[。；;！!？?]', drv_t)
        for s in sents:
            if idiom_t in s or idiom_s in s:
                s_clean = s.strip(' “"”：:，,')
                if 8 <= len(s_clean) <= 60:
                    s_clean = s_clean.replace(idiom_t, '【　　】').replace(idiom_s, '【　　】')
                    return f"{book}載有：「{s_clean}」"
    return None

extracted = {}
for uid, u in db.items():
    extracted[uid] = []
    for it in u['idioms']:
        w = it['idiom']
        ws = t2s.convert(w)
        entry = dict_map.get(ws) or dict_map.get(w)
        ex = None
        drv = None
        exp = ""
        if entry:
            exp = s2t.convert(entry.get('explanation', ''))
            ex = get_real_example(entry, w, ws)
            drv = get_real_derivation(entry, w, ws)
        extracted[uid].append({
            "idiom": w,
            "explanation": exp or it.get('meaning', ''),
            "example": ex,
            "derivation": drv
        })

with open("debug_logs/extracted_real_sentences.json", "w", encoding="utf-8") as f:
    json.dump(extracted, f, ensure_ascii=False, indent=2)

print("Saved extracted sentences.")
