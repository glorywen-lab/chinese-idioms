import json
import re

with open("debug_logs/parsed_80_rows_raw.json", "r", encoding="utf-8") as f:
    all_rows = json.load(f)

# Let's inspect how many items in each row
cleaned_units = {}

# 17 exam units (Rows 1 to 68, each 4 rows)
# Unit 1: 7上1段 (Rows 1-4)
# Unit 2: 7上2段 (Rows 5-8)
# Unit 3: 7上3段 (Rows 9-12)
# Unit 4: 7下1段 (Rows 13-16)
# Unit 5: 7下2段 (Rows 17-20)
# Unit 6: 7下3段 (Rows 21-24)
# Unit 7: 8上1段 (Rows 25-28)
# Unit 8: 8上2段 (Rows 29-32)
# Unit 9: 8上3段 (Rows 33-36)
# Unit 10: 8下1段 (Rows 37-40)
# Unit 11: 8下2段 (Rows 41-44)
# Unit 12: 8下3段 (Rows 45-48)
# Unit 13: 9上1段 (Rows 49-52)
# Unit 14: 9上2段 (Rows 53-56)
# Unit 15: 9上3段 (Rows 57-60)
# Unit 16: 9下1段 (Rows 61-64)
# Unit 17: 9下2段 (Rows 65-68)
# Unit 18: 其實還有(一) (Rows 69-72)
# Unit 19: 其實還有(二) (Rows 73-76)
# Unit 20: 其實還有(三) (Rows 77-80)

exam_names = [
    "7上 第1次段考", "7上 第2次段考", "7上 第3次段考",
    "7下 第1次段考", "7下 第2次段考", "7下 第3次段考",
    "8上 第1次段考", "8上 第2次段考", "8上 第3次段考",
    "8下 第1次段考", "8下 第2次段考", "8下 第3次段考",
    "9上 第1次段考", "9上 第2次段考", "9上 第3次段考",
    "9下 第1次段考", "9下 第2次段考",
    "其實還有 · 拔尖卷(一)", "其實還有 · 拔尖卷(二)", "其實還有 · 終極卷(三)"
]

print("Total exam units:", len(exam_names))
