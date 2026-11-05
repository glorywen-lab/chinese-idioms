# -*- coding: utf-8 -*-
"""
全面檢修並消除全資料庫變式一與變式二（或變式三）語句相似問題：
將 8下 (8_2_1, 8_2_2, 8_2_3) 三個單元全面對齊 7 年級與 9 年級之正統三維架構：
- 變式一（Col 5）：高質感現代生活/情境敘事句（成語自然咬合，杜絕套路）
- 變式二（Col 6）：文化典籍 / 古籍名句（有經典文獻出處，如《詩經》、《左傳》、《史記》、《戰國策》等）
- 變式三（Col 7）：現代校園 / 生活素養（班級日常、同儕、家庭、社會公民）
"""
import json
import os
import sys
sys.path.insert(0, ".")
import scripts.update_unit_8_2_1 as u821
import scripts.update_unit_8_2_2 as u822
import scripts.update_unit_8_2_3 as u823

def apply_all():
    db_path = os.path.join("data", "full_all_units_database.json")
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)

    mapping = {
        "相形見拙": "相形見絀",
        "害羣之馬": "害群之馬",
        "峯迴路轉": "峰迴路轉",
        "殺雞哧猴": "殺雞儆猴",
        "悽風苦雨": "淒風苦雨"
    }

    units_to_apply = [
        ("8_2_1", u821.questions_8_2_1_dict),
        ("8_2_2", u822.questions_8_2_2_dict),
        ("8_2_3", u823.questions_8_2_3_dict)
    ]

    total_updated = 0
    for uid, q_dict in units_to_apply:
        u = db.get(uid)
        if not u:
            print(f"Warning: {uid} not found in db!")
            continue
        for item in u["idioms"]:
            w = item["idiom"]
            lookup_w = mapping.get(w, w)
            if lookup_w in q_dict:
                raw_sents = q_dict[lookup_w]["sentences"]
                # raw_sents[1] is the distinct modern narrative -> 變式一
                # raw_sents[0] is the authentic classical quote -> 變式二
                # raw_sents[2] is the life literacy scenario -> 變式三
                item["sentences"] = [raw_sents[1], raw_sents[0], raw_sents[2]]
                total_updated += 1
            else:
                print(f"Warning: {w} not in {uid} dictionary!")

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"Successfully overhauled {total_updated} idioms in 8下!")

if __name__ == "__main__":
    apply_all()
