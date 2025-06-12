import json
import os
from datetime import datetime

DATA_FILE = "data.json"
BUDGET_FILE = "budget.json"

CATEGORIES = {
    "식비": ["아침", "점심", "저녁", "간식", "카페"],
    "교통": ["버스", "지하철", "택시"],
    "쇼핑": ["의류", "화장품", "잡화"],
    "기타": ["기타"]
}
ALL_CATEGORIES = [item for sublist in CATEGORIES.values() for item in sublist]

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_budget():
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_budget(budget):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budget, f, ensure_ascii=False, indent=2)

def add_record():
    print("가능한 카테고리:")
    for idx, cat in enumerate(ALL_CATEGORIES, 1):
        print(f"{idx}. {cat}", end="  ")
    print()
    try:
        name = input("항목 이름: ").strip()
        amount = int(input("금액 (숫자만): ").strip())
        cat_idx = int(input("카테고리 번호 선택: ").strip()) - 1
        category = ALL_CATEGORIES[cat_idx]
        date = input("날짜 (YYYY-MM-DD): ").strip()
        print("1. 수입   2. 지출")
        kind_input = input("수입/지출 선택 (번호 입력): ").strip()
        if kind_input not in ["1", "2"]:
            raise ValueError
        kind = "수입" if kind_input == "1" else "지출"

        data = load_data()
        record = {
            "name": name,
            "amount": amount,
            "category": category,
            "date": date,
            "type": kind
        }
        data.append(record)
        save_data(data)
        print("✅ 저장 완료!")

        if kind == "지출":
            budget = load_budget()
            spent = sum(d["amount"] for d in data if d["type"] == "지출" and d["category"] == category)
            if category in budget and spent > budget[category]:
                print("⚠️ 예산 초과! 절약 챌린지 실패 처리됨 ❌")

    except (ValueError, IndexError):
        print("❌ 입력 형식 오류: 다시 시도하세요.")

def view_summary():
    data = load_data()
    total_income = sum(d["amount"] for d in data if d["type"] == "수입")
    total_expense = sum(d["amount"] for d in data if d["type"] == "지출")
    print("💼 [전체 수입/지출 요약]")
    print(f"- 총 수입: {total_income}원")
    print(f"- 총 지출: {total_expense}원")
    print(f"- 잔액: {total_income - total_expense}원")

def view_by_category():
    data = load_data()
    summary = {}
    for d in data:
        if d["type"] != "지출":
            continue
        category = d["category"]
        summary[category] = summary.get(category, 0) + d["amount"]
    print("📂 [카테고리별 지출]")
    for cat, amt in summary.items():
        print(f"- {cat}: {amt}원")
    print()

def set_budget():
    print("[예산 설정]")
    for idx, cat in enumerate(ALL_CATEGORIES, 1):
        print(f"{idx}. {cat}", end="  ")
    print()
    try:
        cat_idx = int(input("카테고리 번호 선택: ").strip()) - 1
        category = ALL_CATEGORIES[cat_idx]
        amount = int(input("예산 금액: ").strip())
        budget = load_budget()
        budget[category] = amount
        save_budget(budget)
        print(f"✅ {category} 예산 {amount}원으로 설정 완료")
    except (ValueError, IndexError):
        print("❌ 형식 오류: 다시 입력하세요.")

def monthly_summary():
    data = load_data()
    current_month = datetime.now().strftime("%Y-%m")
    this_month_data = [d for d in data if d["type"] == "지출" and d["date"].startswith(current_month)]
    total = sum(d["amount"] for d in this_month_data)
    category_count = {}
    for d in this_month_data:
        category_count[d["category"]] = category_count.get(d["category"], 0) + d["amount"]
    max_cat = max(category_count, key=category_count.get) if category_count else "없음"
    print("📆 [이번 달 소비 통계]")
    print(f"- 총 지출: {total}원")
    print(f"- 가장 많이 쓴 카테고리: {max_cat}")

def savings_challenge():
    data = load_data()
    daily_spending = {}
    for d in data:
        if d["type"] == "지출":
            day = d["date"]
            daily_spending[day] = daily_spending.get(day, 0) + d["amount"]
    success_days = [day for day, amt in daily_spending.items() if amt <= 10000]
    fail_days = [day for day, amt in daily_spending.items() if amt > 10000]
    print("🎯 [절약 챌린지 결과]")
    print(f"- 성공한 날: {len(success_days)}일 🎉")
    print(f"- 실패한 날: {len(fail_days)}일 ❌")
    if success_days:
        print(f"- 성공 날짜: {', '.join(success_days)}")
    print()

def delete_record():
    data = load_data()
    if not data:
        print("❌ 삭제할 데이터가 없습니다.")
        return
    print("🧹 [기록 삭제]")
    for idx, d in enumerate(data, 1):
        print(f"{idx}. {d['name']} {d['amount']}원 {d['category']} {d['date']} {d['type']}")
    try:
        choice = int(input("삭제할 번호 입력 (0은 취소): ").strip())
        if choice == 0:
            print("삭제 취소됨.")
            return
        removed = data.pop(choice - 1)
        save_data(data)
        print(f"✅ 삭제 완료: {removed['name']} {removed['amount']}원")
    except (ValueError, IndexError):
        print("❌ 잘못된 입력")

def filter_records():
    data = load_data()
    month = input("조회할 월을 입력하세요 (예: 2025-06, Enter 시 전체): ").strip()
    category = input("조회할 카테고리를 입력하세요 (예: 점심, Enter 시 전체): ").strip()

    filtered = data
    if month:
        filtered = [d for d in filtered if d["date"].startswith(month)]
    if category:
        filtered = [d for d in filtered if d["category"] == category]

    total_income = sum(d["amount"] for d in filtered if d["type"] == "수입")
    total_expense = sum(d["amount"] for d in filtered if d["type"] == "지출")
    print("\n📊 [필터 결과]")
    print(f"- 총 수입: {total_income}원")
    print(f"- 총 지출: {total_expense}원 ({len([d for d in filtered if d['type'] == '지출'])}건)")
    print(f"- 잔액: {total_income - total_expense}원")
    if not filtered:
        print("⚠️ 해당 조건의 기록이 없습니다.")

def main():
    while True:
        print("\n💰 BudgetCLI 지출 관리")
        print("1. 수입/지출 입력")
        print("2. 💼 전체 수입/지출 요약")
        print("3. 카테고리별 지출 보기")
        print("4. 💸 예산 설정")
        print("5. 📆 이번 달 소비 통계")
        print("6. 절약 챌린지 결과 보기")
        print("7. 🔥 잘못 입력한 내역 삭제")
        print("8. 🔎 기록 필터 조회")
        print("0. 종료")
        choice = input(">>> ").strip()
        if choice == "1":
            add_record()
        elif choice == "2":
            view_summary()
        elif choice == "3":
            view_by_category()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            savings_challenge()
        elif choice == "7":
            delete_record()
        elif choice == "8":
            filter_records()
        elif choice == "0":
            print("종료합니다.")
            break
        else:
            print("❌ 잘못된 입력")

if __name__ == "__main__":
    main()
