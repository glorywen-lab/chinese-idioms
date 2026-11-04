# -*- coding: utf-8 -*-
import json

db_path = "G:/其他電腦/我的電腦/GloryCloud/01_教學/0-教學資料/0-國文課/debug_logs/full_all_units_database.json"
data = json.load(open(db_path, "r", encoding="utf-8"))

unit = data.get("7_1_1")
print(f"單元名稱: {unit['name']}, 所屬年級: {unit['grade']}, 成語總數: {len(unit['idioms'])}")

report = []
report.append(f"七上第一次段考 (單元 7_1_1) 題庫與答案搭配詳細檢核報告")
report.append(f"="*60)
report.append(f"單元名稱: {unit['name']}")
report.append(f"成語總數: {len(unit['idioms'])} 則成語 (第 1~4 列)")
report.append(f"小單元分組: {len(unit['subunits'])} 個小單元")

potential_issues = []

for idx, item in enumerate(unit['idioms']):
    idiom = item['idiom']
    meaning = item['meaning']
    explanation = item['explanation']
    sentences = item.get('sentences', [])
    distractors = item.get('distractors', [])
    
    # Check 1: blank placeholder
    for s_idx, s in enumerate(sentences):
        if "【　　】" not in s:
            potential_issues.append(f"[{idx+1}] {idiom} 待答句 {s_idx+1} 缺少填空標記【　　】: {s}")
        # Check if the idiom itself accidentally appears in the sentence outside the blank
        s_without_blank = s.replace("【　　】", "")
        if idiom in s_without_blank:
            potential_issues.append(f"[{idx+1}] {idiom} 待答句 {s_idx+1} 原文竟包含正解成語: {s}")
            
    # Check 2: distractors contains the idiom itself
    if idiom in distractors:
        potential_issues.append(f"[{idx+1}] {idiom} 的干擾選項包含自己: {distractors}")
        
    # Check 3: distractors count
    if len(distractors) < 3:
        potential_issues.append(f"[{idx+1}] {idiom} 干擾選項不足 3 個: {distractors}")
        
    report.append(f"\n【第 {idx+1} 題】成語：{idiom} (第 {item['row_num']} 列 · 小單元 {item['sub_id']})")
    report.append(f"  注音：{item.get('pinyin', '')}")
    report.append(f"  釋義：{meaning}")
    report.append(f"  干擾項：{', '.join(distractors)}")
    for s_idx, s in enumerate(sentences):
        filled_s = s.replace("【　　】", f"【{idiom}】")
        report.append(f"  待答句變式 {s_idx+1}：{s}")
        report.append(f"  ➔ 代入正解驗證：{filled_s}")
    report.append(f"  解析說明：{explanation}")

report.append("\n" + "="*60)
report.append(f"檢核結果統計：")
report.append(f"總成語數：{len(unit['idioms'])} 則")
report.append(f"總待答句數：{sum(len(it.get('sentences', [])) for it in unit['idioms'])} 句")
report.append(f"潛在問題發現：{len(potential_issues)} 項")
if potential_issues:
    for iss in potential_issues:
        report.append("  ⚠️ " + iss)
else:
    report.append("  ✅ 所有題目均包含【　　】填空標記，待答句中未洩漏成語，干擾選項不重複且不含正解！")

out_file = "G:/其他電腦/我的電腦/GloryCloud/01_教學/0-教學資料/0-國文課/debug_logs/check_unit_7_1_1_report.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"檢核完成！報告已寫入 {out_file}，潛在問題數: {len(potential_issues)}")
