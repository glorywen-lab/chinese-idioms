import cv2
import numpy as np

# Let's inspect the four tiers:
# tier 29:
# Right to left:
# Col 158: 孤注一擲, 孤芳自賞, 孤苦伶仃, 孤陋寡聞
# Col 159: 孤掌難鳴, 宜室宜家, 屈指可數, 屈尊降貴
# Col 160: 居心叵測, 居安思危, 幸災樂禍, 延頸企踵
# Col 161: 弦外之音, 忠言逆耳, 所向披靡, 承先啟後, 承歡膝下, 拂袖而去
# Col 162: 披沙揀金, 披肝瀝膽, 披星戴月, 披荊斬棘, 披堅執銳, 拋磚引玉
# Col 163: 拈花惹草

# Let's verify each tier by checking against standard dictionary stroke order:
# Notice that each page is organized by STROKE COUNT!
# P9:
# Tier 1: 【八 畫】starts on Tier 2: 里仁為美 (里 is 7 strokes, wait: 【八 畫】 starts after 防微杜漸: 並駕齊驅...)
# Let's check Tier 29:
# 孤 (8 strokes: 子 3 + 瓜 5 = 8 strokes)
# 宜 (8 strokes: 宀 3 + 且 5 = 8 strokes)
# 屈 (8 strokes: 尸 3 + 出 5 = 8 strokes)
# 居 (8 strokes: 尸 3 + 古 5 = 8 strokes)
# 幸 (8 strokes: 土 3 + 𢆉 5 = 8 strokes) -> 幸災樂禍!
# 延 (8 strokes: 廴 2 + 正 5 = 7? or 廴 3 + 5 = 8 strokes) -> 延頸企踵
# 弦 (8 strokes: 弓 3 + 玄 5 = 8 strokes) -> 弦外之音
# 忠 (8 strokes: 中 4 + 心 4 = 8 strokes) -> 忠言逆耳
# 所 (8 strokes: 戶 4 + 斤 4 = 8 strokes) -> 所向披靡
# 承 (8 strokes: 手部 / 8 strokes) -> 承先啟後, 承歡膝下
# 拂 (8 strokes: 扌 3 + 弗 5 = 8 strokes) -> 拂袖而去
# 披 (8 strokes: 扌 3 + 皮 5 = 8 strokes) -> 披沙揀金, 披肝瀝膽, 披星戴月, 披荊斬棘, 披堅執銳
# 拋 (8 strokes: 扌 3 + 8 = 11? or 抛 扌 3 + 5 = 8 strokes) -> 拋磚引玉
# 拈 (8 strokes: 扌 3 + 占 5 = 8 strokes) -> 拈花惹草

# WOW! Every single idiom in Tier 29 has EXACTLY 8 STROKES on the first character!
# Let's verify Tier 29 idioms list:
tier_29 = [
    "孤注一擲", "孤芳自賞", "孤苦伶仃", "孤陋寡聞",
    "孤掌難鳴", "宜室宜家", "屈指可數", "屈尊降貴",
    "居心叵測", "居安思危", "幸災樂禍", "延頸企踵",
    "弦外之音", "忠言逆耳", "所向披靡", "承先啟後",
    "承歡膝下", "拂袖而去", "披沙揀金", "披肝瀝膽",
    "披星戴月", "披荊斬棘", "披堅執銳", "拋磚引玉",
    "拈花惹草"
]
print("Tier 29 count:", len(tier_29))
