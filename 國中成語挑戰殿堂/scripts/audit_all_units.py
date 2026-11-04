# -*- coding: utf-8 -*-
import json

db_path = "G:/其他電腦/我的電腦/GloryCloud/01_教學/0-教學資料/0-國文課/debug_logs/full_all_units_database.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

generic_templates = [
    "面對這次重大的挑戰與考驗，他展現出",
    "在日常生活與求學過程中，我們應當時刻提醒自己切莫",
    "這篇論說文的作者引經據典、構思精妙，字裡行間洋溢著",
    "歷史上凡能成就非凡功業者，無一不是具備",
    "做事若一味投機取巧、不顧後果，最後往往會陷入",
    "從這起社會事件的始末可以清楚看出，如果不具備"
]

total_idioms_all = 0
total_generic_all = 0

print("="*60)
print(f"{'單元名稱':<20} | {'總題數':<8} | {'異常模板題數':<12} | {'異常比例':<8}")
print("="*60)

for u_id, u in db.items():
    total = len(u["idioms"])
    total_idioms_all += total
    generic_count = 0
    for it in u["idioms"]:
        sents = it.get("sentences", [])
        if any(any(gt in s for gt in generic_templates) for s in sents):
            generic_count += 1
    total_generic_all += generic_count
    rate = f"{generic_count / total * 100:.1f}%" if total > 0 else "0%"
    print(f"{u['name']:<20} | {total:<8} | {generic_count:<12} | {rate:<8}")

print("="*60)
print(f"全書 20 單元總計：總成語 {total_idioms_all} 則，異常模板成語 {total_generic_all} 則 ({total_generic_all/total_idioms_all*100:.1f}%)")
