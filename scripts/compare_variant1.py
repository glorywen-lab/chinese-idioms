# -*- coding: utf-8 -*-
import json

with open("data/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

print("=== 7_1_1 變式一 (前 8 題) ===")
for item in db["7_1_1"]["idioms"][:8]:
    print(f"【{item['idiom']}】:\n  {item['sentences'][0]}")

print("\n=== 7_1_2 變式一 (前 5 題) ===")
for item in db["7_1_2"]["idioms"][:5]:
    print(f"【{item['idiom']}】:\n  {item['sentences'][0]}")

print("\n=== 8_1_1 變式一 (前 8 題) ===")
for item in db["8_1_1"]["idioms"][:8]:
    print(f"【{item['idiom']}】:\n  {item['sentences'][0]}")

print("\n=== 8_2_1 變式一 (前 8 題) ===")
for item in db["8_2_1"]["idioms"][:8]:
    print(f"【{item['idiom']}】:\n  {item['sentences'][0]}")
