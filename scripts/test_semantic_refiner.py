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

with open("debug_logs/extracted_real_sentences.json", "r", encoding="utf-8") as f:
    extracted_real = json.load(f)

# Helper to classify polarity and theme from explanation
def analyze_idiom_features(idiom, meaning):
    m = meaning
    # Check polarity
    is_derogatory = any(w in m for w in [
        '貶義', '自私', '貪婪', '驕傲', '自大', '奸詐', '投機', '狡猾', '吝嗇', 
        '凶暴', '虛偽', '殘暴', '陷害', '荒謬', '失敗', '墮落', '惡劣', '卑劣',
        '輕視', '輕浮', '盲目', '糊塗', '短視', '怯懦', '諂媚', '勾結', '狼狽',
        '違法', '壞事', '罪惡', '罪行', '欺騙', '矇蔽', '縱容', '姑息', '窘境'
    ])
    
    is_commendatory = any(w in m for w in [
        '褒義', '高尚', '勇敢', '堅強', '勤奮', '刻苦', '謙遜', '謙虛', '智慧',
        '才華', '忠誠', '正直', '廉潔', '清廉', '團結', '成功', '傑出', '精湛',
        '卓越', '奉獻', '大公無私', '堅忍不拔', '堅持不懈', '深厚', '崇高', '孝順',
        '仁愛', '寬宏大量', '同心協力', '融洽', '和睦', '光明磊落'
    ])
    
    # Specific semantic categories
    cat = 'general'
    if any(w in m for w in ['風景', '景色', '山水', '山川', '春', '秋', '花', '月', '自然', '壯觀', '氣象']):
        cat = 'nature'
    elif any(w in m for w in ['時間', '時光', '歲月', '光陰', '短暫', '迅速', '匆忙', '日久', '長久']):
        cat = 'time'
    elif any(w in m for w in ['讀書', '求學', '文章', '學問', '詩文', '寫作', '字畫', '才學', '書法', '技藝', '文筆']):
        cat = 'study_art'
    elif any(w in m for w in ['團體', '眾人', '軍隊', '作戰', '戰鬥', '勝負', '比賽', '競賽', '球賽']):
        cat = 'cooperation_battle'
    elif any(w in m for w in ['說話', '言語', '議論', '言談', '談吐', '辯論', '誇大', '謊言']):
        cat = 'speech'
    elif any(w in m for w in ['心境', '心情', '憂愁', '喜悅', '憤怒', '驚恐', '擔憂', '神態', '安詳']):
        cat = 'emotion_state'
        
    return {
        'derogatory': is_derogatory,
        'commendatory': is_commendatory,
        'category': cat
    }

# Test sample idioms from 7_1_2, 7_2_1, 8_1_1, 9_1_1
sample_test = ['三令五申', '三年五載', '世外桃源', '扭轉乾坤', '投其所好', '投桃報李', '盛氣凌人', '眼高手低']
results = []
for w in sample_test:
    ws = t2s.convert(w)
    entry = dict_map.get(ws) or dict_map.get(w)
    exp = s2t.convert(entry.get('explanation', '')) if entry else ''
    feat = analyze_idiom_features(w, exp)
    results.append({
        'idiom': w,
        'exp': exp,
        'feat': feat
    })

with open("debug_logs/test_feat_output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Feature analysis test complete.")
