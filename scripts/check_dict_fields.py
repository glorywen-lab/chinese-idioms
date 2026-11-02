import json

with open("debug_logs/xinhua_idioms.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

# check keys of first 5 items
sample_keys = []
for it in dict_data[:5]:
    sample_keys.append({k: (it[k][:40] if isinstance(it[k], str) else it[k]) for k in it})

with open("debug_logs/dict_sample.json", "w", encoding="utf-8") as out:
    json.dump(sample_keys, out, ensure_ascii=False, indent=2)

print("Saved dict_sample.json")
