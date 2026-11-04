# 國中成語挑戰殿堂 · 專案資料庫與網頁系統

> **設計者**：壽山國中 鄭汶瑜 老師  
> **範圍**：國中三年 7上至9下 17 次段考 ＋ 其實還有（共 20 個大單元、80 列、1,435 則成語、4,305 題相異素養情境待答句）  
> **注音標準**：100% 採用臺灣教育部國語審定音標準注音符號（ㄅㄆㄇㄈ）  

---

## 🌐 線上測驗網址 (隨開即測，跨設備免安裝)

👉 **GitHub Pages 線上版**：[https://glorywen-lab.github.io/chinese-idioms/](https://glorywen-lab.github.io/chinese-idioms/)

* 支援手機、平板（iPad/Android）、桌上型電腦與教室觸控大螢幕。
* 具備離線單機運行能力，答題進度、勳章收集與錯題本自動保存在本機瀏覽器。

---

## 📂 本資料夾檔案結構說明

| 檔案 / 目錄 | 類型 | 說明 |
| :--- | :--- | :--- |
| **`index.html`** | 核心主程式 | 雙擊即可在電腦預設瀏覽器（Chrome / Edge）開啟單機離線測驗版。 |
| **`成語大挑戰_8上第2次段考.html`** | 單元特仕版 | 8上第2次段考專用獨立檢測網頁。 |
| **`國中成語挑戰殿堂_題庫總表.xlsx`** | Excel 題庫總表 | **包含 22 個工作表分頁**（20 個段考/拔尖單元各獨立分頁 + 目錄總覽 + 全書總表），方便教師出題與列印。 |
| **`data/`** | 資料目錄 | 收納全書 1,435 則成語資料庫 (`full_all_units_database.json`) 及教育部成語字典語料庫。 |
| **`scripts/`** | 工具腳本 | 收納題庫維護、教育部審定音注音校正、Excel 匯出及 HTML 編譯建置之 Python 腳本。 |

---

## 🛠️ 維護與重新編譯指引

若日後有擴充成語或微調試題，可於本資料夾執行：

1. **校對臺灣注音符號**：
   ```bash
   python scripts/generate_taiwan_zhuyin.py
   ```
2. **驗證題庫品質與空格完整性**：
   ```bash
   python scripts/verify_database_quality.py
   ```
3. **重新匯出 20 單元分頁 Excel 總表**：
   ```bash
   python scripts/export_to_excel.py
   ```
4. **重新編譯網頁主程式**：
   ```bash
   python scripts/build_full_application.py
   ```
