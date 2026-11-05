# -*- coding: utf-8 -*-
import json

meta = json.load(open("meta_quotes_detailed.json", encoding="utf-8"))
print(f"Total meta items: {len(meta)}")
for idx, m in enumerate(meta, 1):
    print(f"{idx:2d}. [{m['uid']}][{m['idiom']}][變式{m['variant']}] 原引號內: 「{m['quote']}」")
