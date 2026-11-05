# -*- coding: utf-8 -*-
import json

with open("quotes_to_fix.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

meta_patterns = ['遂以', '遂演為', '遂稱', '遂成', '引申為', '演為', '故稱', '故以', '是為', '實為', '可謂', '堪稱', '這正是', '此之謂', '此【　　】', '真可謂', '成【　　】', '為【　　】之', '【　　】之喻', '後遂以', '後世遂以', '何其【　　】', '豈可【　　】']

meta_list = []
for q in quotes:
    for p in meta_patterns:
        if p in q['quote']:
            meta_list.append(q)
            break

print(f"Total: {len(meta_list)}")
with open("meta_quotes_detailed.json", "w", encoding="utf-8") as f:
    json.dump(meta_list, f, ensure_ascii=False, indent=2)

for item in meta_list:
    print(f"[{item['uid']}][{item['idiom']}][變式{item['variant']}] {item['full']}")
