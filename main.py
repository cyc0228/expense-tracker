"""
專案名稱：個人記帳系統 (Expense Tracker)
描述：提供新增消費、查看紀錄、統計總支出等功能的命令列應用程式。
作者：[你的名字/暱稱]
"""

import json
import os
from datetime import datetime

# 取得 main.py 所在的資料夾絕對路徑
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 將 JSON 檔案名稱與專案資料夾路徑綁定
# FILE_PATH = os.path.join(BASE_DIR, "expenses.json")

class ExpenseTracker:
    def __init__(self, filename = "expense.json"):
        self.filename = filename
        self.records = self.load_data()  # 啟動時自動載入資料

    def load_data(self):
        """從 JSON 檔案載入歷史紀錄"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        """將紀錄儲存至 JSON 檔案"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        
    def add_expense(self, category: str, amount: int, note: str = ""):
        """新增一筆消費紀錄（含時間）"""
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        expense = {"date":date_str, "category": category, "amount": amount, "note": note}

        self.records.append(expense)
        self.save_data()
        print(f"\n 成功新增消費：【{category}】${amount} ({note if note else '無備註'})({date_str})")

    def delete_expense(self, index: int):
        """刪除指定編號的消費紀錄"""
        if not self.records:
            print("目前沒有任何紀錄可供刪除！")
            return

        # 檢查輸入的數字是否在範圍內 (1 ~ 資料總筆數)
        if 1 <= index <= len(self.records):
            removed_item = self.records.pop(index - 1)
            self.save_data()
            print(f"\n 已成功刪除：【{removed_item['category']}】${removed_item['amount']}")
        else:
            print("\n 無法刪除！找不到該編號，請確認後重新輸入。")    
        
    def show_records(self):
        """顯示所有消費紀錄"""
        print("\n---目前的所有消費紀錄 ---")
        if not self.records:
            print("目前還沒有任何消費紀錄！")
            return
            
        total = 0
        for i, item in enumerate(self.records, 1):
            date = item.get("date", "無日期")
            note_str = item['note'] if item['note'] else "無備註"
            print(f"{i}. [{date}] 類別: {item['category']:<6} | 金額: ${item['amount']:<5} | 備註: {note_str}")
            total += item['amount']
        print(f"-" * 50)
        print(f"總支出：${total}\n")

    def edit_expense(self, index: int, new_category: str = "", new_amount: int = None, new_note: str = None):
        """修改指定編號的消費紀錄"""
        if not self.records:
            print("目前沒有任何紀錄可供修改！")
            return

        if 1 <= index <= len(self.records):
            item = self.records[index - 1]
            
            # 如果使用者有輸入新內容才更新，留白（空字串/None）就保留舊值
            if new_category:
                item["category"] = new_category
            if new_amount is not None:
                item["amount"] = new_amount
            if new_note is not None:
                item["note"] = new_note

            self.save_data() 
            print("\n 修改成功！更新後的紀錄為：")
            date = item.get("date", "無日期")
            print(f"[{date}] 類別: {item['category']} | 金額: ${item['amount']} | 備註: {item['note']}")
        else:
            print("\n 找不到該編號，請重新確認！")

    def show_category_summary(self):
        """分類統計與分析"""
        if not self.records:
            print("目前沒有任何紀錄可供統計！")
            return

        summary = {}
        total_all = 0

        # 計算每個類別的加總金額
        for item in self.records:
            category = item["category"]
            amount = item["amount"]
            summary[category] = summary.get(category, 0) + amount
            total_all += amount

        print("\n=== 各類別消費統計與分析 ===")
        for category, amount in summary.items():
            # 計算佔總支出的百分比
            percentage = (amount / total_all) * 100 if total_all > 0 else 0
            print(f"【{category:<6}】: ${amount:<6} (佔比: {percentage:.1f}%)")
        print("-" * 35)
        print(f"總累計支出：${total_all}\n")

    def check_monthly_budget(self, budget: int):
        """月預算警示（根據當前年月過濾）"""
        current_month = datetime.now().strftime("%Y-%m")  # 取得如 "2026-08"
        monthly_total = 0

        for item in self.records:
            date_str = item.get("date", "")
            # 比對日期開頭是否與當前年月吻合
            if date_str.startswith(current_month):
                monthly_total += item["amount"]

        print(f"\n=== 本月 ({current_month}) 預算監控 ===")
        print(f"本月已消費：${monthly_total} / 設定預算：${budget}")

        if monthly_total > budget:
            over = monthly_total - budget
            print(f" 警告！本月支出已【超支 ${over}】！請注意控制開銷。")
        else:
            remaining = budget - monthly_total
            print(f" 本月預算狀況正常，尚餘可用額度：${remaining}\n")

def main():
    """主程式入口點"""
    tracker = ExpenseTracker()
    print("=== 歡迎使用個人記帳系統 ===")
    
    while True:
        print("=== 個人記帳系統 ===")
        print("1. 新增消費")
        print("2. 查看所有消費")
        print("3. 刪除消費紀錄")
        print("4. 修改消費紀錄")
        print("5. 查看分類統計")
        print("6. 設定/檢查月預算")
        print("7. 離開程式")
        choice = input("請選擇功能 (1-7): ").strip()

        if choice == "1":
            category = input("請輸入消費類別（例如：晚餐、交通）：")

            while True:
                try:
                    amount = int(input("請輸入消費金額："))
                    if amount <= 0:
                        print("金額必須大於 0，請重新輸入！")
                        continue
                    break  # 輸入成功，跳出金額輸入迴圈
                except ValueError:
                    print("格式錯誤！請輸入純數字金額（例如：120）。")
            
            note = input("請輸入備註（直接按 Enter 可省略）：")
            
            tracker.add_expense(category, amount, note)
            
        elif choice == "2":
            tracker.show_records()

        elif choice == "3":
            tracker.show_records()
            if tracker.records:
                while True:
                    try:
                        num = int(input("請輸入想要刪除的紀錄編號："))
                        tracker.delete_expense(num)
                        break
                    except ValueError:
                        print("格式錯誤！請輸入純數字編號（例如：1）。")

        elif choice == "4":
            tracker.show_records()
            if tracker.records:
                try:
                    num = int(input("請輸入要修改的紀錄編號："))
                    if 1 <= num <= len(tracker.records):
                        print("\n提示：直接按 Enter 可保留原本的資料不修改")
                        
                        category_input= input("新類別（留白不改）：").strip()
                        
                        amount_str = input("新金額（留白不改）：").strip()
                        amount = int(amount_str) if amount_str else None  # 沒填就帶 None
                        
                        note_input = input("新備註（留白不改）：")
                        note = note_input if note_input != "" else None

                        tracker.edit_expense(num, new_category = category_input, new_amount = amount, new_note = note)
                    else:
                        print("找不到該編號！")
                except ValueError:
                    print("金額格式錯誤！請輸入純數字。")

        elif choice == "5":
            tracker.show_category_summary()

        elif choice == "6":
            while True:
                try:
                    budget_input = int(input("請輸入本月的目標預算上限（如：15000）："))
                    tracker.check_monthly_budget(budget_input)
                    break
                except ValueError:
                    print("格式錯誤！請輸入純數字金額。")

        elif choice == "7":
            print("感謝使用，程式已關閉！")
            break
        else:
            print("輸入錯誤，請重新選擇！\n")


# 確保這個檔案是被直接執行，而不是被其他檔案 import 時才執行
if __name__ == "__main__":
    main()
