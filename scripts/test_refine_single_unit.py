# -*- coding: utf-8 -*-
import json
import re
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

with open("debug_logs/xinhua_idioms.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

dict_map = {}
for it in dict_data:
    dict_map[it['word']] = it
    dict_map[s2t.convert(it['word'])] = it

def clean_example(ex_raw, idiom):
    if not ex_raw or ex_raw in ['无', '無']:
        return None
    ex_t = s2t.convert(ex_raw)
    ex_clean = re.sub(r'★.*', '', ex_t).strip()
    ex_clean = re.sub(r'《.*?》.*', '', ex_clean).strip()
    ex_clean = re.sub(r'（.*?）.*', '', ex_clean).strip()
    ex_clean = ex_clean.strip(' “"”：:，,')
    if len(ex_clean) < 10:
        return None
    if '～' in ex_clean:
        return ex_clean.replace('～', '【　　】')
    if idiom in ex_clean:
        return ex_clean.replace(idiom, '【　　】')
    return None

def clean_derivation(drv_raw, idiom):
    if not drv_raw or drv_raw in ['无', '無']:
        return None
    drv_t = s2t.convert(drv_raw)
    # Match patterns like: 《史記·項羽本紀》... quote ...
    m = re.search(r'([《〈][^》〉]+[》〉][^：:「“"”]*)[：:「“"\s]+(.+?)[」”"]', drv_t)
    if m:
        src = m.group(1).strip()
        quote = m.group(2).strip()
        if len(quote) >= 8 and (idiom in quote or '～' in quote):
            q_clean = quote.replace(idiom, '【　　】').replace('～', '【　　】')
            return f"{src}名句：「{q_clean}」"
    # Fallback to book + sentence containing idiom
    m_book = re.search(r'([《〈][^》〉]+[》〉])', drv_t)
    if m_book and idiom in drv_t:
        book = m_book.group(1)
        sents = re.split(r'[。；;！!？?]', drv_t)
        for s in sents:
            if idiom in s:
                s_c = s.strip(' “"”：:，,')
                if 10 <= len(s_c) <= 60:
                    return f"{book}載有名言：「{s_c.replace(idiom, '【　　】')}」"
    return None

def generate_contextual_sentences(idiom, meaning):
    m = meaning
    sents = []
    
    # 1. 道德修養 / 堅毅正直 (褒義)
    if any(k in m for k in ['高尚', '勇敢', '堅強', '勤奮', '刻苦', '謙遜', '謙虛', '智慧', '忠誠', '正直', '清廉', '廉潔', '卓越', '大公無私', '堅忍不拔', '光明磊落', '忠心', '正派', '修養']):
        sents.append(f"他在工作崗位上克盡職責、廉潔自持，始終展現出【　　】的崇高品格，深得大家的敬佩。")
        sents.append(f"面對重大的利益考驗，他毫不動搖，堅持【　　】的原則，贏得社會各界的一致讚譽。")
        sents.append(f"求學與做人應當以古聖先賢為榜樣，時刻涵養【　　】的胸襟與美德。")
        
    # 2. 負面批判 / 警戒警惕 (貶義)
    elif any(k in m for k in ['自私', '貪婪', '驕傲', '自大', '奸詐', '投機', '狡猾', '吝嗇', '凶暴', '虛偽', '殘暴', '陷害', '荒謬', '失敗', '墮落', '惡劣', '卑劣', '輕視', '輕浮', '盲目', '糊塗', '短視', '怯懦', '諂媚', '勾結', '違法', '罪惡', '欺騙', '矇蔽', '縱容', '姑息', '窘境', '貶義']):
        sents.append(f"做人處事應當誠信踏實，切莫【　　】，否則一旦失去大家的信任，便難以在團體中立足。")
        sents.append(f"團體合作中最忌諱有人【　　】、推諉責任，大家應當齊心協力才能圓滿達成目標。")
        sents.append(f"這名不肖商人為了謀取暴利竟做出【　　】的勾當，最終受到法律的嚴懲與社會的唾棄。")
        
    # 3. 讀書做學問 / 文學藝能
    elif any(k in m for k in ['讀書', '求學', '文章', '學問', '詩文', '寫作', '字畫', '才學', '書法', '技藝', '文筆', '才華', '精湛', '博學', '見聞']):
        sents.append(f"學習任何專業技藝都必須下苦功夫扎實練習，才能達到【　　】的精湛境界。")
        sents.append(f"這部文學巨作描寫生動細膩、思想深邃，字裡行間處處可見作者【　　】的深厚功力。")
        sents.append(f"求學不可只知死記硬背，唯有融會貫通並能靈活運用，方能展現【　　】的真實學養。")
        
    # 4. 自然風光 / 景物氣候
    elif any(k in m for k in ['風景', '景色', '山水', '山川', '春', '秋', '花', '月', '自然', '壯觀', '氣象', '優美', '景致']):
        sents.append(f"週末全家出遊漫步在秀麗的山林步道，遠眺四周【　　】的壯闊景致，令人頓覺心曠神怡。")
        sents.append(f"清晨的湖畔薄霧繚繞、水波不興，眼前這幅【　　】的如畫美景，吸引了許多攝影愛好者駐足流連。")
        sents.append(f"歷經漫長寒冬，大地漸漸回暖，草木萌芽展現出【　　】的勃勃生機。")
        
    # 5. 時間流逝 / 歲月光陰
    elif any(k in m for k in ['時間', '時光', '歲月', '光陰', '短暫', '迅速', '匆忙', '日久', '長久', '多年', '長年']):
        sents.append(f"國中三年的求學時光在歡笑中飛逝，轉眼即將畢業，回首往事真令人有【　　】之感慨。")
        sents.append(f"掌握一門精湛手藝絕非幾天就能速成，往往需要經過【　　】的不斷淬鍊與積累。")
        sents.append(f"時光匆匆如白駒過隙，面對【　　】的歲月更迭，我們更應珍惜青春、把握當下。")
        
    # 6. 團體合作 / 人際互動 / 比賽競技
    elif any(k in m for k in ['團結', '眾人', '軍隊', '作戰', '戰鬥', '勝負', '比賽', '競賽', '球賽', '朋友', '友誼', '和睦', '協同']):
        sents.append(f"在拔河比賽的緊要關頭，全班同學【　　】、奮力拚搏，終於在加油聲中勇奪冠軍。")
        sents.append(f"鄰里同儕之間應當互相尊重包容，秉持【　　】的精神，生活環境才能更加祥和美好。")
        sents.append(f"面對強勁的競爭對手，隊員們毫不畏縮，發揮【　　】的團隊默契，贏得了最終的勝利。")
        
    # 7. 處事策劃 / 防微杜漸 / 變通靈活
    elif any(k in m for k in ['防範', '預防', '準備', '策劃', '辦法', '方針', '規則', '靈活', '變通', '周密', '謹慎', '小心']):
        sents.append(f"颱風季節來臨之前，防汛單位早已做好【　　】的各項整備措施，以確保民眾生命財產安全。")
        sents.append(f"做事情應當周全規劃、步步為營，懂得【　　】的道理，才能避免臨事手忙腳亂。")
        sents.append(f"處理複雜問題不可墨守成規，必須依據客觀情勢【　　】，方能找到最佳的解決方案。")
        
    # 8. 狀態、情態、情緒描述 (通用客觀)
    else:
        sents.append(f"面對生活中的種種考驗與變化，我們若能抱持【　　】的從容態度，往往能迎刃而解。")
        sents.append(f"經過警方與社區居民的深入調查，這起離奇事件的真相終於【　　】。")
        sents.append(f"做事必須按部就班、循序漸進，唯有秉持【　　】的踏實作風，才能奠定穩固成功的基石。")
        
    return sents

# Let's test refining 7_1_2
with open("debug_logs/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

u = db["7_1_2"]
refined_712 = []
for it in u["idioms"]:
    w = it["idiom"]
    ws = t2s.convert(w)
    entry = dict_map.get(w) or dict_map.get(ws)
    m = it.get("meaning", "")
    if entry and len(entry.get("explanation", "")) > len(m):
        m = s2t.convert(entry.get("explanation"))
        
    ex = clean_example(entry.get("example"), w) if entry else None
    drv = clean_derivation(entry.get("derivation"), w) if entry else None
    ctx_sents = generate_contextual_sentences(w, m)
    
    final_sents = []
    if ex:
        final_sents.append(ex)
    if drv:
        final_sents.append(drv)
        
    for cs in ctx_sents:
        if len(final_sents) >= 3:
            break
        if cs not in final_sents:
            final_sents.append(cs)
            
    # Guarantee 3 sentences
    while len(final_sents) < 3:
        final_sents.append(f"在日常學習與生活中，我們應當深刻體會【　　】所蘊含的哲理與意涵。")
        
    refined_712.append({
        "idiom": w,
        "meaning": m,
        "sentences": final_sents[:3]
    })

with open("debug_logs/preview_refined_712.json", "w", encoding="utf-8") as f:
    json.dump(refined_712[:10], f, ensure_ascii=False, indent=2)

print("Saved preview for 7_1_2 first 10 idioms.")
