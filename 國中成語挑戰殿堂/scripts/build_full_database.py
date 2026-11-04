import json
import re
import random
import opencc

s2t = opencc.OpenCC('s2t')

with open("debug_logs/cleaned_80_rows.json", "r", encoding="utf-8") as f:
    all_rows = json.load(f)

with open("debug_logs/questions_multi_8_2.json", "r", encoding="utf-8") as f:
    existing_8_2 = json.load(f)

existing_8_2_map = {it['idiom']: it for it in existing_8_2}

# Define 20 Units
unit_definitions = [
    {"id": "7_1_1", "name": "7上 第1次段考", "grade": "七年級上學期", "rows": [1, 2, 3, 4]},
    {"id": "7_1_2", "name": "7上 第2次段考", "grade": "七年級上學期", "rows": [5, 6, 7, 8]},
    {"id": "7_1_3", "name": "7上 第3次段考", "grade": "七年級上學期", "rows": [9, 10, 11, 12]},
    {"id": "7_2_1", "name": "7下 第1次段考", "grade": "七年級下學期", "rows": [13, 14, 15, 16]},
    {"id": "7_2_2", "name": "7下 第2次段考", "grade": "七年級下學期", "rows": [17, 18, 19, 20]},
    {"id": "7_2_3", "name": "7下 第3次段考", "grade": "七年級下學期", "rows": [21, 22, 23, 24]},
    {"id": "8_1_1", "name": "8上 第1次段考", "grade": "八年級上學期", "rows": [25, 26, 27, 28]},
    {"id": "8_1_2", "name": "8上 第2次段考", "grade": "八年級上學期", "rows": [29, 30, 31, 32]},
    {"id": "8_1_3", "name": "8上 第3次段考", "grade": "八年級上學期", "rows": [33, 34, 35, 36]},
    {"id": "8_2_1", "name": "8下 第1次段考", "grade": "八年級下學期", "rows": [37, 38, 39, 40]},
    {"id": "8_2_2", "name": "8下 第2次段考", "grade": "八年級下學期", "rows": [41, 42, 43, 44]},
    {"id": "8_2_3", "name": "8下 第3次段考", "grade": "八年級下學期", "rows": [45, 46, 47, 48]},
    {"id": "9_1_1", "name": "9上 第1次段考", "grade": "九年級上學期", "rows": [49, 50, 51, 52]},
    {"id": "9_1_2", "name": "9上 第2次段考", "grade": "九年級上學期", "rows": [53, 54, 55, 56]},
    {"id": "9_1_3", "name": "9上 第3次段考", "grade": "九年級上學期", "rows": [57, 58, 59, 60]},
    {"id": "9_2_1", "name": "9下 第1次段考", "grade": "九年級下學期", "rows": [61, 62, 63, 64]},
    {"id": "9_2_2", "name": "9下 第2次段考", "grade": "九年級下學期", "rows": [65, 66, 67, 68]},
    {"id": "extra_1", "name": "其實還有 · 拔尖卷(一)", "grade": "進階高手擴充", "rows": [69, 70, 71, 72]},
    {"id": "extra_2", "name": "其實還有 · 拔尖卷(二)", "grade": "進階高手擴充", "rows": [73, 74, 75, 76]},
    {"id": "extra_3", "name": "其實還有 · 終極卷(三)", "grade": "進階高手擴充", "rows": [77, 78, 79, 80]}
]

# Life / School / History sentence templates for synthetic generation
sentence_templates = [
    "面對這次重大的挑戰與考驗，他展現出【　　】的胸襟與氣魄，深獲全體師長與同學的肯定。",
    "在日常生活與求學過程中，我們應當時刻提醒自己切莫【　　】，腳踏實地方能走得長遠。",
    "這篇論說文的作者引經據典、構思精妙，字裡行間洋溢著【　　】的神采，令人讀來回味無窮。",
    "歷史上凡能成就非凡功業者，無一不是具備【　　】的意志與格局，方能在變局中立於不敗之地。",
    "做事若一味投機取巧、不顧後果，最後往往會陷入【　　】的窘境，大家務必引以為戒。",
    "從這起社會事件的始末可以清楚看出，如果不具備【　　】的憂患意識，危難來臨時便難以招架。"
]

full_units_data = {}

for u_idx, u in enumerate(unit_definitions, 1):
    u_id = u["id"]
    u_name = u["name"]
    u_grade = u["grade"]
    u_rows = u["rows"]
    
    # Collect all idioms in this unit
    unit_idioms = []
    subunits = []
    
    for sub_idx, r_num in enumerate(u_rows, 1):
        r_str = str(r_num)
        row_idiom_objs = all_rows.get(r_str, {}).get("idioms", [])
        
        # Build subunit metadata
        sample_names = "、".join([it['idiom'] for it in row_idiom_objs[:6]]) + ("..." if len(row_idiom_objs) > 6 else "")
        subunits.append({
            "sub_id": sub_idx,
            "row_num": r_num,
            "row_name": f"第 {r_num} 列",
            "title": f"小單元 {sub_idx} (第 {r_num} 列)",
            "sample_idioms": sample_names,
            "count": len(row_idiom_objs)
        })
        
        for it in row_idiom_objs:
            w = it['idiom']
            # If we already have handcrafted data in 8上2段, prioritize it!
            if w in existing_8_2_map:
                item_data = existing_8_2_map[w]
                unit_idioms.append({
                    "sub_id": sub_idx,
                    "row_num": r_num,
                    "idiom": w,
                    "pinyin": item_data.get("pinyin", it.get("pinyin", "")),
                    "meaning": item_data.get("meaning", s2t.convert(it.get("explanation", ""))),
                    "sentences": item_data.get("sentences", []),
                    "explanation": item_data.get("explanation", s2t.convert(it.get("explanation", "")))
                })
            else:
                # Generate rich sentences
                meaning = s2t.convert(it.get("explanation", "")).strip()
                if not meaning:
                    meaning = f"形容具有「{w}」之義的典故與語意。"
                
                # Try to use example from dict if available
                sentences = []
                ex = s2t.convert(it.get("example", "")).strip()
                if ex and ex != "無" and len(ex) > 10:
                    ex_clean = re.sub(r'★.*', '', ex).strip()
                    if '～' in ex_clean:
                        sentences.append(ex_clean.replace('～', '【　　】'))
                    elif w in ex_clean:
                        sentences.append(ex_clean.replace(w, '【　　】'))
                        
                # Add synthetic sentences to make at least 3
                tpl_picks = random.sample(sentence_templates, 3)
                for tpl in tpl_picks:
                    if len(sentences) >= 3: break
                    sentences.append(tpl)
                    
                deriv = s2t.convert(it.get("derivation", "")).strip()
                exp_text = f"「{w}」意為：{meaning}。"
                if deriv and deriv != "無":
                    exp_text += f" 出處典故：{deriv}。"
                    
                unit_idioms.append({
                    "sub_id": sub_idx,
                    "row_num": r_num,
                    "idiom": w,
                    "pinyin": it.get("pinyin", ""),
                    "meaning": meaning,
                    "sentences": sentences,
                    "explanation": exp_text
                })
                
    # Generate distractors for each idiom in this unit
    all_unit_names = [it['idiom'] for it in unit_idioms]
    for it in unit_idioms:
        same_pool = [x for x in all_unit_names if x != it['idiom']]
        if len(same_pool) >= 3:
            it['distractors'] = random.sample(same_pool, 3)
        else:
            it['distractors'] = ["一心一意", "井底之蛙", "守株待兔"]
            
    full_units_data[u_id] = {
        "id": u_id,
        "name": u_name,
        "grade": u_grade,
        "subunits": subunits,
        "total_idioms": len(unit_idioms),
        "idioms": unit_idioms
    }

print("Full units built:", len(full_units_data))
with open("debug_logs/full_all_units_database.json", "w", encoding="utf-8") as f:
    json.dump(full_units_data, f, ensure_ascii=False)

print("Saved full_all_units_database.json")
