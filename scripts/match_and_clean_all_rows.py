import json
import re
import opencc

s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

# Load Xinhua idioms
with open("debug_logs/xinhua_idioms.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

# Build lookup table: trad_word -> entry
# Also normalized lookup (no whitespace, standard chars)
dict_lookup = {}
for entry in dict_data:
    w_trad = s2t.convert(entry['word'])
    dict_lookup[w_trad] = entry
    # also simplified
    dict_lookup[entry['word']] = entry

print(f"Dictionary index built with {len(dict_lookup)} keys.")

with open("debug_logs/parsed_80_rows_raw.json", "r", encoding="utf-8") as f:
    all_rows = json.load(f)

# Helper function to find best match in dictionary
def find_idiom(candidate, fallback_prefix=None):
    c_trad = s2t.convert(candidate)
    if c_trad in dict_lookup:
        return s2t.convert(dict_lookup[c_trad]['word']), dict_lookup[c_trad]
    
    # If length is 3 and fallback_prefix is given
    if len(c_trad) == 3 and fallback_prefix:
        with_pre = fallback_prefix + c_trad
        if with_pre in dict_lookup:
            return s2t.convert(dict_lookup[with_pre]['word']), dict_lookup[with_pre]
            
    # Try fuzzy match (1 char difference for 4-char string)
    if len(c_trad) == 4:
        for w in dict_lookup.keys():
            if len(w) == 4:
                diff = sum(1 for a, b in zip(c_trad, w) if a != b)
                if diff <= 1:
                    # check if first 2 or last 2 match
                    if c_trad[:2] == w[:2] or c_trad[2:] == w[2:]:
                        return s2t.convert(dict_lookup[w]['word']), dict_lookup[w]
                        
    # Try with prefix fuzzy
    if len(c_trad) == 3 and fallback_prefix:
        with_pre = fallback_prefix + c_trad
        for w in dict_lookup.keys():
            if len(w) == 4:
                diff = sum(1 for a, b in zip(with_pre, w) if a != b)
                if diff <= 1:
                    return s2t.convert(dict_lookup[w]['word']), dict_lookup[w]

    return None, None

cleaned_80_rows = {}
total_matched = 0
unmatched_list = []

for r_str, row_obj in all_rows.items():
    r = int(r_str)
    raw_items = row_obj['items']
    
    # Detect predominant 1st character in 4-char words of this row (e.g. 一, 不, 自, 無...)
    first_chars = [it[0] for it in raw_items if len(it) == 4]
    from collections import Counter
    c_counts = Counter(first_chars)
    common_prefix = c_counts.most_common(1)[0][0] if c_counts and c_counts.most_common(1)[0][1] >= 3 else None
    
    row_matched_idioms = []
    seen_in_row = set()
    
    for item in raw_items:
        # clean item
        t = re.sub(r'[\d【】\[\]\s,\.。;；]', '', item)
        if not t: continue
        
        # Sometimes 2 idioms joined together: len == 8
        candidates = [t]
        if len(t) == 8:
            candidates = [t[:4], t[4:]]
            
        for cand in candidates:
            matched_name, entry = find_idiom(cand, common_prefix)
            if matched_name and matched_name not in seen_in_row:
                seen_in_row.add(matched_name)
                row_matched_idioms.append({
                    'idiom': matched_name,
                    'pinyin': entry.get('pinyin', ''),
                    'explanation': entry.get('explanation', ''),
                    'derivation': entry.get('derivation', '')
                })
                total_matched += 1
            elif not matched_name and len(cand) >= 3:
                unmatched_list.append((r, cand))
                
    cleaned_80_rows[r] = {
        'row_id': r,
        'printed_page': row_obj['printed_page'],
        'tier_in_page': row_obj['tier_in_page'],
        'count': len(row_matched_idioms),
        'idioms': row_matched_idioms
    }

print(f"Total matched idioms: {total_matched}")
print(f"Total unmatched raw candidates: {len(unmatched_list)}")

with open("debug_logs/cleaned_80_rows.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_80_rows, f, ensure_ascii=False, indent=2)

with open("debug_logs/cleaning_summary.txt", "w", encoding="utf-8") as out:
    for r in range(1, 81):
        if r in cleaned_80_rows:
            row = cleaned_80_rows[r]
            idiom_names = [it['idiom'] for it in row['idioms']]
            out.write(f"Row {r:02d} (P.{row['printed_page']:02d} T{row['tier_in_page']}): {row['count']:2d} idioms | {' '.join(idiom_names)}\n")

print("Saved cleaned_80_rows.json and cleaning_summary.txt")
