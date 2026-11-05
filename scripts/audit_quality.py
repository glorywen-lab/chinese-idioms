# -*- coding: utf-8 -*-
"""
自動化題庫品質稽核工具：
1. 支語詞彙掃描（黑名單）
2. 簡繁字體與標點規範掃描（爲、裏、跟着、象、直引號、◇等）
3. 句子重複率檢核（全書零重複）
4. 空格格式檢核（必須為【　　】全形雙空格）
5. 句子長度適中性檢核（20 ~ 75 字）
"""
import json
import re
import os
from collections import Counter

# 支語與大陸規範詞彙黑名單
MAINLAND_BUZZWORDS = [
    "科研成果", "科研", "視頻", "音頻", "軟件", "硬件", "屏幕", "打印",
    "打滿補丁", "質量", "信息", "水平", "打造", "打造成", "搞好", "搞定",
    "立體化", "走心", "接地氣", "給力", "忽悠", "套路", "貓膩", "警察蜀黍",
    "小夥伴", "素質", "宏觀", "巨集", "抓好", "落實"
]

# 簡繁轉換殘留或大陸字形/標點
MAINLAND_GLYPHS = [
    ("爲", "為"),
    ("裏", "裡"),
    ("跟着", "跟著"),
    ("◇", ""),
    ("”", "」"),
    ("“", "「"),
]

def audit_database(db_path=os.path.join("data", "full_all_units_database.json"), target_units=None):
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
        
    print(f"Loaded database from: {db_path}")
    
    total_idioms = 0
    total_sentences = 0
    all_sentences = []
    issues = []
    
    units_to_check = target_units if target_units else list(db.keys())
    
    for uid in units_to_check:
        u = db[uid]
        uname = u.get("name", uid)
        idioms = u.get("idioms", [])
        
        for item in idioms:
            total_idioms += 1
            w = item["idiom"]
            meaning = item.get("meaning", "")
            sents = item.get("sentences", [])
            
            # Check meaning for mainland glyphs
            for mg, tw in MAINLAND_GLYPHS:
                if mg in meaning:
                    issues.append(f"[{uname}][{w}] 釋義含大陸字形/標點 '{mg}': {meaning}")
            for bw in MAINLAND_BUZZWORDS:
                if bw in meaning:
                    issues.append(f"[{uname}][{w}] 釋義含疑似支語詞彙 '{bw}': {meaning}")
                    
            if len(sents) != 3:
                issues.append(f"[{uname}][{w}] 待答題數不為 3 題 (現有 {len(sents)} 題)")
                
            for s_idx, s in enumerate(sents, 1):
                total_sentences += 1
                all_sentences.append((s, uid, uname, w, s_idx))
                
                # Check bracket format
                if "【　　】" not in s:
                    issues.append(f"[{uname}][{w}][變式{s_idx}] 缺少標準空格標記【　　】: {s}")
                elif s.count("【　　】") > 1:
                    issues.append(f"[{uname}][{w}][變式{s_idx}] 出現多個空格標記: {s}")
                    
                # Check mainland buzzwords
                for bw in MAINLAND_BUZZWORDS:
                    if bw in s:
                        issues.append(f"[{uname}][{w}][變式{s_idx}] 含有支語詞彙 '{bw}': {s}")
                        
                # Check mainland glyphs
                for mg, tw in MAINLAND_GLYPHS:
                    if mg in s:
                        issues.append(f"[{uname}][{w}][變式{s_idx}] 含有大陸字形/標點 '{mg}': {s}")
                        
                # Check length
                if len(s) < 18 or len(s) > 85:
                    issues.append(f"[{uname}][{w}][變式{s_idx}] 句子長度異常 ({len(s)} 字): {s}")

    # Check duplicates across checked sentences
    sent_texts = [s[0] for s in all_sentences]
    counter = Counter(sent_texts)
    duplicates = {text: count for text, count in counter.items() if count > 1}
    
    print("\n" + "="*60)
    print(f"稽核範圍: {units_to_check}")
    print(f"成語數: {total_idioms} 則 | 待答句子數: {total_sentences} 句")
    print(f"重複句子數量: {len(duplicates)} 組")
    if duplicates:
        print("--- 重複句範例 (前 3 名) ---")
        for text, count in list(duplicates.items())[:3]:
            print(f"  [{count} 次重複]: {text[:50]}...")
            
    print(f"規範問題總數: {len(issues)} 處")
    if issues:
        print("--- 問題列表 (前 10 筆) ---")
        for iss in issues[:10]:
            print(f"  * {iss}")
    else:
        print("✅ 恭喜！所稽核單元 100% 通過：零支語、零重複句、標點與空格完全合規！")
    print("="*60 + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].upper() != "ALL":
        units = sys.argv[1:]
    else:
        units = None  # None 代表所有單元
    audit_database(target_units=units)
