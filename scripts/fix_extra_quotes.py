# -*- coding: utf-8 -*-
import json
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "data", "full_all_units_database.json")
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

fixes = {
    ("7_2_3", "形形色色", 1): "《列子·天瑞》探討天地萬物之演化：「形形者不形，色色者不色」。後世常以【　　】形容事物種類繁多、各具型態。",
    ("8_2_1", "時來運轉", 2): "明代凌濛初《初刻拍案驚奇》開篇勸世詩：「困厄莫教休，時來運自周」。後世遂以【　　】勉勵困頓之人堅守希望期待轉機。",
    ("8_2_2", "秦晉之好", 2): "元代喬吉《金錢記》雜劇讚頌兩姓聯姻之勝事：「兩家結為秦晉之好，天作之合」。後世遂以【　　】祝賀新人喜締良緣。",
    ("8_2_3", "得魚忘荃", 2): "《莊子·外物》論言意之道名言：「荃者所以在魚，得魚而忘荃；蹄者所以在兔，得兔而忘蹄；言者所以在意，得意而忘言」。後世遂稱【　　】。",
    ("9_2_2", "養虎留患", 2): "《史記·項羽本紀》載張良勸劉邦追擊項羽名言：「今釋弗擊，此所謂『養虎自遺患』也」。後遂演為成語【　　】。"
}

count = 0
for (uid, w, v_idx), s in fixes.items():
    if uid in db:
        for item in db[uid]["idioms"]:
            if item["idiom"] == w:
                item["sentences"][v_idx - 1] = s
                count += 1
                break

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"Successfully fixed {count}/{len(fixes)} extra classical quotes!")
