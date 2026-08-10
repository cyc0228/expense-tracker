# 📊 Personal Expense Tracker (CLI Version 1.0)

一個使用 Python 開發的命令列個人記帳系統，支援完整的 CRUD 操作、JSON 資料持久化儲存、自動時間標記與財務分析功能。

## ✨ 核心功能

- 📝 **消費紀錄管理 (CRUD)**：新增、查詢、刪除與動態修改消費紀錄。
- ⏰ **自動時間標記**：整合 `datetime` 模組，新增消費時自動紀錄當下年月日時分。
- 💾 **資料持久化**：使用 `json` 模組存取資料，並以絕對路徑處理跨平台檔案存取。
- 📊 **分類統計與分析**：自動計算各類別支出金額與百分比佔比（%）。
- ⚠️ **月預算監控警示**：精準過濾當月消費，即時提示是否超支或剩餘額度。
- 🛡️ **輸入防呆與格式化**：具備 `try-except` 異常處理與輸入字串修剪機制。

## 🛠️ 使用技術

- **Language:** Python 3.10+
- **Standard Libraries:** `json`, `os`, `datetime`

## 🚀 快速開始

1. 複製專案庫：
   ```bash
   git clone [https://github.com/cyc0228/expense-tracker.git](https://github.com/cyc0228/expense-tracker.git)
   cd expense-tracker