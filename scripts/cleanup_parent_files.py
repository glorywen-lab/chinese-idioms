# -*- coding: utf-8 -*-
import os
import shutil
import datetime

parent_dir = r"G:\其他電腦\我的電腦\GloryCloud\01_教學\0-教學資料\0-國文課"
project_dir = r"G:\其他電腦\我的電腦\GloryCloud\01_教學\0-教學資料\0-國文課\國中成語挑戰殿堂"
archive_dir = os.path.join(project_dir, "archive", f"parent_dir_cleanup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
os.makedirs(archive_dir, exist_ok=True)

targets = [
    ".gitignore",
    "index.html",
    "成語大挑戰_8上第2次段考.html",
    "國中成語挑戰殿堂_題庫總表.xlsx",
    "README.md",
    ".keep"
]

results = []
for fname in targets:
    p = os.path.join(parent_dir, fname)
    if os.path.exists(p):
        # 1. 備份到 archive
        backup_path = os.path.join(archive_dir, fname)
        shutil.copy2(p, backup_path)
        # 2. 刪除父目錄檔案
        os.remove(p)
        results.append((fname, True, "已封存並成功刪除"))
    else:
        results.append((fname, False, "檔案不存在"))

print("Clean up finished:")
for fname, success, msg in results:
    print(f"  {fname:35s}: {msg}")
