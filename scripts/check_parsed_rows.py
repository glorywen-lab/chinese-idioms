import json

with open("debug_logs/parsed_80_rows_raw.json", "r", encoding="utf-8") as f:
    all_rows = json.load(f)

with open("debug_logs/rows_summary.txt", "w", encoding="utf-8") as out:
    out.write(f"Total rows parsed: {len(all_rows)}\n\n")
    for r_str, row in all_rows.items():
        r = int(r_str)
        out.write(f"Row {r:02d} (P.{row['printed_page']:02d} Tier {row['tier_in_page']}): {len(row['items']):2d} items | {' '.join(row['items'])}\n")

print("Saved rows_summary.txt")
