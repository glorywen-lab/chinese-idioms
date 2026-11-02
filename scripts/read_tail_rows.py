import json

with open("debug_logs/parsed_80_rows_raw.json", "r", encoding="utf-8") as f:
    all_rows = json.load(f)

# Let's inspect the remaining rows in debug_logs/rows_summary.txt
# Read rows 45 to 80
with open("debug_logs/rows_summary.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("debug_logs/rows_45_80.txt", "w", encoding="utf-8") as out:
    out.writelines(lines[45:])

print("Saved rows_45_80.txt, total lines:", len(lines))
