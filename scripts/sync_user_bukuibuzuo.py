# -*- coding: utf-8 -*-
import json

db_path = "data/full_all_units_database.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

u = db["7_1_2"]
for item in u["idioms"]:
    if item["idiom"] in ["不愧不作", "不愧不怍"]:
        print(f"Updating idiom from '{item['idiom']}' to '不愧不怍'")
        item["idiom"] = "不愧不怍"
        item["pinyin"] = "ㄅㄨˋ ㄎㄨㄟˋ ㄅㄨˋ ㄗㄨㄛˋ"
        item["meaning"] = "光明磊落，問心無愧。愧、怍，皆指內心慚愧羞恥。源自《孟子·盡心上》。"
        item["sentences"] = [
            "只要我們行事坦蕩、凡事盡心盡力，哪怕最終成果不如預期，亦可做到俯仰無愧、【　　】。",
            "孟子提出君子有三樂，其中第二樂便是「仰不愧於天，俯不怍於人」，這正是【　　】的人生極致境界。",
            "身為新聞記者當為公眾捍衛真相，面對各方強大施壓亦不曲解報導，方能【　　】於這份崇高志業。"
        ]

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Database permanently synced with user's '不愧不怍'!")
