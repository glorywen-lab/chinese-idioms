# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook("國中成語挑戰殿堂_題庫總表.xlsx")
for sheetname in wb.sheetnames:
    ws = wb[sheetname]
    for row in ws.iter_rows(values_only=True):
        if row and any("不愧" in str(cell) or "不怍" in str(cell) for cell in row if cell):
            print(f"Sheet: {sheetname}")
            print(f"Row data: {row}")
