# -*- coding: utf-8 -*-
import json

db_path = "debug_logs/full_all_units_database.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

print("="*50)
for uid, u in db.items():
    print(f"{uid:10} | {u['name']:25} | {len(u['idioms']):4} idioms")
print("="*50)
print(f"Total units: {len(db)}, Total idioms: {sum(len(u['idioms']) for u in db.values())}")
