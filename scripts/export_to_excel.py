# -*- coding: utf-8 -*-
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

db_path = "G:/其他電腦/我的電腦/GloryCloud/01_教學/0-教學資料/0-國文課/debug_logs/full_all_units_database.json"
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

wb = openpyxl.Workbook()
wb.remove(wb.active)  # Remove default blank sheet

# Color palettes
fill_dark_green = PatternFill(start_color="1E3F20", end_color="1E3F20", fill_type="solid")
fill_moss_green = PatternFill(start_color="2D5A27", end_color="2D5A27", fill_type="solid")
fill_light_row = PatternFill(start_color="F8FAF8", end_color="F8FAF8", fill_type="solid")
fill_summary_hdr = PatternFill(start_color="854D0E", end_color="854D0E", fill_type="solid")

font_header = Font(name="微軟正黑體", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="微軟正黑體", size=10, bold=True, color="102018")
font_normal = Font(name="微軟正黑體", size=10, color="292524")
font_idiom = Font(name="標楷體", size=12, bold=True, color="132E1B")
font_answer = Font(name="微軟正黑體", size=11, bold=True, color="166534")

thin_border = Border(
    left=Side(style="thin", color="D6D3D1"),
    right=Side(style="thin", color="D6D3D1"),
    top=Side(style="thin", color="D6D3D1"),
    bottom=Side(style="thin", color="D6D3D1")
)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

# -------------------------------------------------------------
# 1. 建立首頁：單元架構與目錄總覽 (Overview Sheet)
# -------------------------------------------------------------
ws_summary = wb.create_sheet(title="單元架構與目錄總覽")
ws_summary.views.sheetView[0].showGridLines = True
ws_summary.freeze_panes = "A2"

summary_headers = ["單元代碼", "單元全稱", "工作表分頁名稱", "成語總題數", "待答題庫變式數", "備註說明"]
ws_summary.append(summary_headers)
ws_summary.row_dimensions[1].height = 28

for col_num in range(1, len(summary_headers) + 1):
    c = ws_summary.cell(row=1, column=col_num)
    c.fill = fill_summary_hdr
    c.font = font_header
    c.alignment = align_center
    c.border = thin_border

sheet_name_mapping = {
    "7_1_1": "7上-第1次段考",
    "7_1_2": "7上-第2次段考",
    "7_1_3": "7上-第3次段考",
    "7_2_1": "7下-第1次段考",
    "7_2_2": "7下-第2次段考",
    "7_2_3": "7下-第3次段考",
    "8_1_1": "8上-第1次段考",
    "8_1_2": "8上-第2次段考",
    "8_1_3": "8上-第3次段考",
    "8_2_1": "8下-第1次段考",
    "8_2_2": "8下-第2次段考",
    "8_2_3": "8下-第3次段考",
    "9_1_1": "9上-第1次段考",
    "9_1_2": "9上-第2次段考",
    "9_1_3": "9上-第3次段考",
    "9_2_1": "9下-第1次段考",
    "9_2_2": "9下-第2次段考",
    "extra_1": "其實還有-拔尖卷一",
    "extra_2": "其實還有-拔尖卷二",
    "extra_3": "其實還有-終極卷三"
}

total_idioms_all = 0
total_sentences_all = 0

for u_idx, (uid, u) in enumerate(db.items(), 2):
    count = len(u["idioms"])
    s_count = count * 3
    total_idioms_all += count
    total_sentences_all += s_count
    sh_name = sheet_name_mapping.get(uid, u["name"][:30])
    
    row_vals = [
        uid,
        u["name"],
        sh_name,
        count,
        s_count,
        "教育部《成語典》嚴選 · 臺灣教育部注音符號 · 3組相異情境句 (文學/典籍/生活素養)"
    ]
    ws_summary.append(row_vals)
    ws_summary.row_dimensions[u_idx].height = 24
    
    for c_idx in range(1, len(summary_headers) + 1):
        cell = ws_summary.cell(row=u_idx, column=c_idx)
        cell.border = thin_border
        if c_idx in [1, 3]:
            cell.font = font_bold
            cell.alignment = align_center
        elif c_idx in [4, 5]:
            cell.font = font_answer
            cell.alignment = align_center
        elif c_idx == 2:
            cell.font = font_normal
            cell.alignment = align_left
        else:
            cell.font = font_normal
            cell.alignment = align_left
            
        if u_idx % 2 == 0:
            cell.fill = fill_light_row

# Summary total row
total_row_idx = len(db) + 2
ws_summary.append(["全書總計", "20 個大單元", "20 個獨立分頁", total_idioms_all, total_sentences_all, "全書 1,435 則成語 · 4,305 題待答庫 100% 精修"])
ws_summary.row_dimensions[total_row_idx].height = 28
for c_idx in range(1, len(summary_headers) + 1):
    cell = ws_summary.cell(row=total_row_idx, column=c_idx)
    cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    cell.font = Font(name="微軟正黑體", size=11, bold=True, color="92400E")
    cell.border = thin_border
    cell.alignment = align_center if c_idx in [1, 3, 4, 5] else align_left

# Set summary col widths
sum_col_widths = [14, 25, 22, 14, 16, 45]
for i, w in enumerate(sum_col_widths, 1):
    ws_summary.column_dimensions[get_column_letter(i)].width = w

# -------------------------------------------------------------
# 2. 建立 20 個單元各自獨立的分頁 (20 Unit Worksheets)
# -------------------------------------------------------------
unit_headers = [
    "序號", "成語正字", "臺灣注音符號", "教育部標準釋義",
    "待答題 (變式一·經典文學)", "待答題 (變式二·古籍名句)", "待答題 (變式三·生活素養)",
    "標準答案"
]

all_rows_for_master = []

for uid, u in db.items():
    sh_title = sheet_name_mapping.get(uid, u["name"][:30])
    ws = wb.create_sheet(title=sh_title)
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "A2"
    
    # Header
    ws.append(unit_headers)
    ws.row_dimensions[1].height = 28
    for col_num in range(1, len(unit_headers) + 1):
        c = ws.cell(row=1, column=col_num)
        c.fill = fill_moss_green
        c.font = font_header
        c.alignment = align_center
        c.border = thin_border
        
    for idx, it in enumerate(u["idioms"], 1):
        sents = it.get("sentences", [])
        s1 = sents[0] if len(sents) > 0 else ""
        s2 = sents[1] if len(sents) > 1 else ""
        s3 = sents[2] if len(sents) > 2 else ""
        w = it.get("idiom", "")
        py = it.get("zhuyin", "")
        meaning = it.get("meaning", "")
        
        row_data = [idx, w, py, meaning, s1, s2, s3, w]
        ws.append(row_data)
        
        # Save for master sheet
        all_rows_for_master.append([
            len(all_rows_for_master) + 1,
            u["name"],
            sh_title,
            w,
            py,
            meaning,
            s1,
            s2,
            s3,
            w
        ])
        
        row_idx = idx + 1
        ws.row_dimensions[row_idx].height = 46
        
        for c_idx in range(1, len(unit_headers) + 1):
            cell = ws.cell(row=row_idx, column=c_idx)
            cell.border = thin_border
            if c_idx == 1:
                cell.font = font_bold
                cell.alignment = align_center
            elif c_idx == 2:
                cell.font = font_idiom
                cell.alignment = align_center
            elif c_idx == 3:
                cell.font = font_normal
                cell.alignment = align_center
            elif c_idx == 8:
                cell.font = font_answer
                cell.alignment = align_center
            else:
                cell.font = font_normal
                cell.alignment = align_left
                
            if row_idx % 2 == 0:
                cell.fill = fill_light_row
                
    # Column widths for unit sheet
    col_widths = [8, 14, 18, 32, 38, 38, 38, 14]
    for i, w_val in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w_val

# -------------------------------------------------------------
# 3. 建立最後一頁：全書 1,435 題完整題庫總表 (Master Sheet)
# -------------------------------------------------------------
ws_master = wb.create_sheet(title="全書1435題完整總表")
ws_master.views.sheetView[0].showGridLines = True
ws_master.freeze_panes = "A2"

master_headers = [
    "全書題號", "單元全稱", "所屬分頁", "成語正字", "臺灣注音符號", "標準釋義",
    "待答題 (變式一·經典文學)", "待答題 (變式二·古籍名句)", "待答題 (變式三·生活素養)",
    "標準答案"
]

ws_master.append(master_headers)
ws_master.row_dimensions[1].height = 28
for col_num in range(1, len(master_headers) + 1):
    c = ws_master.cell(row=1, column=col_num)
    c.fill = fill_dark_green
    c.font = font_header
    c.alignment = align_center
    c.border = thin_border

for r_idx, r_data in enumerate(all_rows_for_master, 2):
    ws_master.append(r_data)
    ws_master.row_dimensions[r_idx].height = 42
    
    for c_idx in range(1, len(master_headers) + 1):
        cell = ws_master.cell(row=r_idx, column=c_idx)
        cell.border = thin_border
        if c_idx in [1, 3]:
            cell.font = font_bold
            cell.alignment = align_center
        elif c_idx == 4:
            cell.font = font_idiom
            cell.alignment = align_center
        elif c_idx in [5, 10]:
            cell.font = font_answer if c_idx == 10 else font_normal
            cell.alignment = align_center
        elif c_idx == 2:
            cell.font = font_bold
            cell.alignment = align_left
        else:
            cell.font = font_normal
            cell.alignment = align_left
            
        if r_idx % 2 == 0:
            cell.fill = fill_light_row

master_col_widths = [10, 20, 18, 14, 18, 30, 38, 38, 38, 14]
for i, w_val in enumerate(master_col_widths, 1):
    ws_master.column_dimensions[get_column_letter(i)].width = w_val

# -------------------------------------------------------------
# Save workbook
# -------------------------------------------------------------
output_excel_path = "G:/其他電腦/我的電腦/GloryCloud/01_教學/0-教學資料/0-國文課/國中成語挑戰殿堂_題庫總表.xlsx"
wb.save(output_excel_path)
print(f"Excel workbook successfully generated at: {output_excel_path}")
print(f"Total sheets: {len(wb.sheetnames)} sheets (Overview + 20 Units + Master)")
