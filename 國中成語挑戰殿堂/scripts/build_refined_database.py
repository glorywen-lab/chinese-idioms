# -*- coding: utf-8 -*-
import json
import re
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

# Load raw dictionary
with open("debug_logs/xinhua_idioms.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

dict_map = {}
for it in dict_data:
    dict_map[it['word']] = it
    w_t = s2t.convert(it['word'])
    dict_map[w_t] = it

# Load full database
with open("debug_logs/full_all_units_database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

# Helper to clean example
def clean_example_sent(ex_raw, idiom):
    if not ex_raw or ex_raw in ['无', '無']:
        return None
    ex_t = s2t.convert(ex_raw)
    ex_t = re.sub(r'★.*', '', ex_t).strip()
    ex_t = re.sub(r'《.*?》.*', '', ex_t).strip()
    ex_t = re.sub(r'（.*?）.*', '', ex_t).strip()
    ex_t = ex_t.strip(' “"”：:，,')
    if len(ex_t) < 10 or len(ex_t) > 90:
        return None
    if '～' in ex_t:
        return ex_t.replace('～', '【　　】')
    if idiom in ex_t:
        return ex_t.replace(idiom, '【　　】')
    return None

# Helper to clean derivation quote
def clean_derivation_sent(drv_raw, idiom):
    if not drv_raw or drv_raw in ['无', '無']:
        return None
    drv_t = s2t.convert(drv_raw)
    
    # Try pattern: 《Book》... quote with idiom ...
    # e.g. 《史記·項羽本紀》：「...」
    m_book = re.search(r'([《〈][^》〉]+[》〉])', drv_t)
    if not m_book:
        return None
    book = m_book.group(1)
    
    # Look for quotes in derivation
    quotes = re.findall(r'[「“"]([^」”"]+)[」”"]', drv_t)
    for q in quotes:
        if idiom in q and 8 <= len(q) <= 60:
            return f"{book}名句：「{q.replace(idiom, '【　　】')}」"
            
    # Look for sentences containing idiom in derivation
    sents = re.split(r'[。；;！!？?]', drv_t)
    for s in sents:
        if idiom in s:
            s_clean = s.strip(' “"”：:，,')
            # remove leading book titles if present
            s_clean = re.sub(r'^[《〈][^》〉]+[》〉]', '', s_clean).strip(' “"”：:，,')
            if 8 <= len(s_clean) <= 60:
                return f"{book}典籍載有名言：「{s_clean.replace(idiom, '【　　】')}」"
                
    return None

# Specialized 8_1_2 fixes for 紆尊降貴, 朋比為奸, 虎視眈眈
fixed_8_1_2 = {
    "紆尊降貴": [
        "這位享譽國際的知名學者【　　】，親自來到偏鄉小學為孩子們說故事，展現十足親和力。",
        "董事長平日待人謙遜，在員工運動會上【　　】與基層同仁一同組隊接力，毫無架子。",
        "他總擺出一副高高在上的傲慢姿態，彷彿跟一般同仁打招呼都是【　　】似的，令人反感。"
    ],
    "朋比為奸": [
        "這幾名不肖官員與黑心商人【　　】，私下收受鉅額賄賂並掏空公款，終究難逃法網制裁。",
        "檢調機關經過長達半年的嚴密蒐證，終於將這夥【　　】的跨國詐騙集團一網打盡。",
        "若任由少數害群之馬在團體中【　　】、營私舞弊，必將嚴重損害全體同仁的共同信譽。"
    ],
    "虎視眈眈": [
        "周遭各國對這塊蘊藏豐富礦產的戰略要地【　　】，邊境防禦工事絲毫不敢懈怠。",
        "這家老字號企業一旦出現資金周轉不靈，各方競爭對手勢必會【　　】，企圖強行低價收購。",
        "非洲大草原上的獵豹隱匿在灌木叢後，【　　】地緊盯著落單的羚羊，伺機展開突襲。"
    ]
}

# Fine-grained semantic scenario generator
def generate_fine_scenarios(idiom, meaning):
    m = meaning
    sents = []
    
    # 1. 傲慢驕橫、自大自滿
    if any(k in m for k in ['驕傲', '傲慢', '自滿', '目中無人', '不可一世', '自高自大', '驕矜', '盛氣', '跋扈']):
        sents.append(f"他自從獲得競賽冠軍後便漸生驕氣，平日待人接物總是【　　】，引起許多同學的反感。")
        sents.append(f"求學與做人貴在虛懷若谷，若取得一點小成績就【　　】，最後往往會在競爭中慘遭滑鐵盧。")
        sents.append(f"這名主管依仗著長官的賞識便【　　】，完全不聽取基層員工的建言，導致團隊向心力盡失。")
        
    # 2. 貪婪自私、唯利是圖、吝嗇
    elif any(k in m for k in ['貪婪', '自私', '唯利是圖', '吝嗇', '金錢', '暴利', '橫財', '不肯付出', '小氣']):
        sents.append(f"做人處事切莫【　　】，只顧自身利益而不顧團體死活，終將失去身邊所有真心的朋友。")
        sents.append(f"那名黑心廠商被利益蒙蔽了良心，竟做出【　　】的缺德勾當，遭到檢調單位全面法辦。")
        sents.append(f"他坐擁千萬家產卻對任何慈善公益活動【　　】，令人不禁搖頭嘆息其為人之冷漠。")
        
    # 3. 虛偽欺騙、奸詐狡猾、作惡多端
    elif any(k in m for k in ['虛偽', '欺騙', '奸詐', '狡猾', '勾結', '暗中', '玩弄', '串通', '作惡', '陷害', '謊言']):
        sents.append(f"在陽光透明的現代社會中，任何人企圖【　　】來瞞騙大眾，終究是紙包不住火的。")
        sents.append(f"這場採購公開標案竟然有人試圖【　　】動手腳，司法機關已主動介入調閱所有卷宗。")
        sents.append(f"與人交往最重視真誠坦率，如果一味【　　】、口蜜腹劍，久而久之必為眾人所唾棄。")
        
    # 4. 懶惰懈怠、投機取巧、短視近利
    elif any(k in m for k in ['懶惰', '懈怠', '投機', '取巧', '不肯下功夫', '短視', '不勞而獲', '坐享其成']):
        sents.append(f"求學沒有任何捷徑可走，唯有腳踏實地苦讀，切莫心存僥倖企圖【　　】。")
        sents.append(f"他平日不肯認真打底，總想靠著【　　】來應付考試，結果成績一公布便原形畢露。")
        sents.append(f"做事若只圖眼前方便而【　　】，往往會為未來的發展埋下巨大的隱患與危機。")
        
    # 5. 堅毅不拔、勤奮刻苦、勇敢無畏 (褒義大德)
    elif any(k in m for k in ['堅毅', '勤奮', '刻苦', '勇敢', '無畏', '不屈', '刻苦鑽研', '孜孜不倦', '毅力', '奮勇', '堅強']):
        sents.append(f"在面對一次又一次的失敗與打擊時，他憑藉著【　　】的精神，終於逆境重生創造奇蹟。")
        sents.append(f"為了在全國技能競賽中脫穎而出，選手們連續半年【　　】地反覆操練，汗水灑滿練習場。")
        sents.append(f"面對洶湧的洪流與肆虐的風雨，救災人員【　　】地挺進災區，全力搜救受困居民。")
        
    # 6. 正直清廉、大公無私、高風亮節
    elif any(k in m for k in ['正直', '清廉', '廉潔', '大公無私', '光明磊落', '剛正', '高尚', '清高', '廉政']):
        sents.append(f"他擔任法官數十年始終秉公執法、【　　】，深受法界同仁與社會大眾的尊崇與景仰。")
        sents.append(f"身為採購主管，他面對包商重金行賄毫不動心，始終堅守【　　】的職業道德底線。")
        sents.append(f"這位長者一生行事坦蕩、【　　】，為後輩子孫樹立了最值得效法的品德風範。")
        
    # 7. 讀書求學、學識淵博、技藝爐火純青
    elif any(k in m for k in ['學問', '讀書', '淵博', '求學', '文章', '著作', '技藝', '精湛', '書法', '畫作', '文思', '才華', '造詣']):
        sents.append(f"老工匠將畢生精力奉獻給傳統木雕藝術，刀工刀法早已達到【　　】的出神入化境界。")
        sents.append(f"這部劃時代的經典文學巨著情節引人入勝、文字洗鍊，堪稱【　　】的不朽名篇。")
        sents.append(f"王教授在學術界耕耘數十年，涉獵廣泛且造詣深厚，展現了【　　】的大家學者風範。")
        
    # 8. 自然景致、山川秀麗、氣象景觀
    elif any(k in m for k in ['風景', '景色', '山川', '山水', '自然', '秀麗', '壯觀', '氣象', '江河', '春光', '秋景']):
        sents.append(f"清晨漫步於如夢似幻的湖畔小徑，微風拂面、水光瀲灩，眼前【　　】的風光令人心醉。")
        sents.append(f"這座與世隔絕的深山村落四周青山綠水環抱，宛如隱身塵囂之外的【　　】。")
        sents.append(f"登臨泰山極頂極目遠眺，雲海翻騰、群峰聳立，好一幅【　　】的壯麗山河畫卷！")
        
    # 9. 時間光陰、歲月滄桑、轉瞬即逝
    elif any(k in m for k in ['時間', '光陰', '歲月', '短暫', '迅速', '匆忙', '日久', '多年', '轉眼', '長久']):
        sents.append(f"國中三年的青春求學生涯在歡聲笑語中匆匆度過，回首往事真有【　　】之感慨。")
        sents.append(f"練就一項高超卓越的專利技術絕非朝夕之功，非得經過【　　】的千錘百鍊不可。")
        sents.append(f"光陰荏苒如白駒過隙，面對【　　】的飛逝歲月，我們唯有奮發圖強方能不負韶華。")
        
    # 10. 團結協作、齊心合力、同舟共濟
    elif any(k in m for k in ['團結', '同心', '齊心', '合力', '合作', '協同', '眾人', '共同', '互助']):
        sents.append(f"在拔河總決賽的白熱化關鍵時刻，全班隊員【　　】、死守防線，終於拿下勝利錦旗。")
        sents.append(f"面對突如其來的嚴重天災，全國軍民【　　】、攜手互助，共同展開艱鉅的重建家園工程。")
        sents.append(f"專案小組成員秉持【　　】的團隊精神，群策群力解決了軟體系統開發上的重大難題。")
        
    # 11. 謹慎周密、未雨綢繆、防患未然
    elif any(k in m for k in ['防範', '預防', '準備', '防備', '謹慎', '周密', '小心', '未雨綢繆', '警惕']):
        sents.append(f"強烈颱風即將登陸，防颱指揮中心早已做好各項【　　】的周全應變措施以減少災情。")
        sents.append(f"投資理財不可盲目跟風冒進，事先做好風險評估與資產配置，才是【　　】的上策。")
        sents.append(f"處事講究防微杜漸，在危機尚未擴大蔓延之前懂得【　　】，方能徹底化解災禍於無形。")
        
    # 12. 說話言談、議論辯駁
    elif any(k in m for k in ['說話', '言語', '議論', '言談', '辯駁', '陳述', '誇張', '話語', '談話']):
        sents.append(f"他在辯論賽場上思路清晰、引經據典，一番【　　】的精彩陳詞令評審與全場觀眾為之折服。")
        sents.append(f"公眾人物對社會具有深遠影響力，發言時務必慎言謹行，切莫【　　】引發無謂的社會紛擾。")
        sents.append(f"聽了專家這番【　　】的剖析與解說，眾人終於茅塞頓開，完全解開了心中的長久疑惑。")
        
    # 13. 心情神態、情緒反應
    elif any(k in m for k in ['心境', '心情', '高興', '悲傷', '憂愁', '害怕', '驚恐', '神色', '容貌', '態度']):
        sents.append(f"得知自己的作品在國際影展中榮獲首獎時，導演不禁【　　】地流下了喜悅的淚水。")
        sents.append(f"在成績揭曉前夕，大家在考場外【　　】，屏氣凝神地注視著公布欄上的榜單。")
        sents.append(f"面對評審突如其來的犀利提問，他依舊神色自若、【　　】，冷靜從容地應對作答。")
        
    # 14. 困境挫折、走投無路、危急關頭
    elif any(k in m for k in ['困境', '窘境', '危機', '走投無路', '困難', '危急', '挫折', '窘迫', '危險']):
        sents.append(f"這家跨國巨擘因決策連連失誤導致資金斷鏈，如今已陷入【　　】的破產危機之中。")
        sents.append(f"在球隊落後二十分的【　　】下，全體隊員依然咬緊牙關奮戰到底，絕不輕言放棄。")
        sents.append(f"若不及時遏止這種破壞生態環境的惡行，人類將來必將嚐到【　　】的苦果。")
        
    # 15. 通用客觀狀態、事物發展規律
    else:
        sents.append(f"這項重大科研成果凝聚了研究團隊多年的心血結晶，絕非一蹴可幾，可說是【　　】的展現。")
        sents.append(f"經過警方與鑑識人員日以繼夜的抽絲剝繭調查，這起迷霧重重的懸案終於【　　】。")
        sents.append(f"做學問與做人相同，必須按部就班扎實積累，唯有秉持【　　】的態度才能行穩致遠。")
        
    return sents

# Now let's loop through all units and refine everything
refined_db = {}
stats = {"total": 0, "ex_used": 0, "drv_used": 0, "synthesized": 0}

for uid, u in db.items():
    refined_u = {
        "name": u["name"],
        "tier_range": u.get("tier_range", ""),
        "idioms": []
    }
    
    # 7_1_1 is already hand-crafted to perfection! Keep 100% untouched!
    if uid == "7_1_1":
        refined_u["idioms"] = u["idioms"]
        refined_db[uid] = refined_u
        stats["total"] += len(u["idioms"])
        continue
        
    for it in u["idioms"]:
        stats["total"] += 1
        w = it["idiom"]
        ws = t2s.convert(w)
        entry = dict_map.get(w) or dict_map.get(ws)
        
        # Check meaning
        m = it.get("meaning", "")
        if entry:
            exp_t = s2t.convert(entry.get("explanation", ""))
            if len(exp_t) > len(m):
                m = exp_t
                
        # If in 8_1_2 and in fixed list
        if uid == "8_1_2" and w in fixed_8_1_2:
            refined_u["idioms"].append({
                "idiom": w,
                "pinyin": it.get("pinyin", ""),
                "zhuyin": it.get("zhuyin", ""),
                "meaning": m,
                "sentences": fixed_8_1_2[w]
            })
            continue
            
        # If in 8_1_2 and already good (no generic templates), keep!
        if uid == "8_1_2":
            old_sents = it.get("sentences", [])
            has_generic = any(any(gt in s for gt in [
                "面對這次重大的挑戰與考驗，他展現出",
                "在日常生活與求學過程中，我們應當時刻提醒自己切莫",
                "這篇論說文的作者引經據典、構思精妙，字裡行間洋溢著",
                "歷史上凡能成就非凡功業者，無一不是具備",
                "做事若一味投機取巧、不顧後果，最後往往會陷入",
                "從這起社會事件的始末可以清楚看出，如果不具備"
            ]) for s in old_sents)
            if not has_generic and len(old_sents) == 3:
                refined_u["idioms"].append(it)
                continue
                
        # Build 3 high-quality sentences
        s_candidates = []
        
        # Candidate 1: Real literature example
        if entry:
            ex_s = clean_example_sent(entry.get("example"), w)
            if ex_s:
                s_candidates.append(ex_s)
                stats["ex_used"] += 1
                
        # Candidate 2: Real derivation quote
        if entry:
            drv_s = clean_derivation_sent(entry.get("derivation"), w)
            if drv_s:
                s_candidates.append(drv_s)
                stats["drv_used"] += 1
                
        # Fill remaining with contextual scenarios
        ctx_list = generate_fine_scenarios(w, m)
        for cs in ctx_list:
            if len(s_candidates) >= 3:
                break
            if cs not in s_candidates:
                s_candidates.append(cs)
                stats["synthesized"] += 1
                
        # Ensure exactly 3 sentences
        while len(s_candidates) < 3:
            s_candidates.append(f"在生活與學習的歷程中，我們應當深刻體悟【　　】所傳達的哲理智慧與深刻意涵。")
            
        refined_u["idioms"].append({
            "idiom": w,
            "pinyin": it.get("pinyin", ""),
            "zhuyin": it.get("zhuyin", ""),
            "meaning": m,
            "sentences": s_candidates[:3]
        })
        
    refined_db[uid] = refined_u

with open("debug_logs/full_all_units_database.json", "w", encoding="utf-8") as f:
    json.dump(refined_db, f, ensure_ascii=False, indent=2)

print("Finished refining full database!")
print(f"Stats: Total={stats['total']}, Real Examples={stats['ex_used']}, Real Derivations={stats['drv_used']}, Synthesized Contexts={stats['synthesized']}")
