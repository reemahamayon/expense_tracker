import os
import re
import json
from datetime import datetime
from decimal import Decimal

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))


def get_file_path(name):
    """Each user gets their own file, e.g. zoobiya_expenses.json"""
    safe = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "user"
    return os.path.join(BASE_FOLDER, f"{safe}_expenses.json")


def load_expenses(path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(path, expenses):
    with open(path, "w") as file:
        json.dump(expenses, file, indent=4)


def read_amount(text):
    """Find the number inside text like 'Rs 1,200.50' or '10 T'.
    Returns (amount, was_exact). Raises ValueError if no valid number."""
    match = re.search(r"\d[\d,]*\.?\d*|\.\d+", text)
    if not match:
        raise ValueError("No number found")
    amount = Decimal(match.group().replace(",", ""))
    if amount <= 0:
        raise ValueError("Amount must be above zero")
    return amount, text.strip() == match.group()


def calculate_total(expenses):
    total = Decimal("0")  # initialized OUTSIDE the loop
    for item in expenses:
        total = total + Decimal(item["amount"])  # the accumulator pattern
    return total


def show_expenses(expenses):
    if not expenses:
        print("\nNo expenses yet.")
        return
    print(f"\n{'ID':<5}{'Amount':>12}  {'Note':<20}{'Date'}")
    print("-" * 60)
    for item in expenses:
        amount = Decimal(item["amount"])
        print(f"{item['id']:<5}{amount:>12.2f}  {item['note']:<20}{item['date']}")
    print("-" * 60)
    print(f"{'TOTAL':<5}{calculate_total(expenses):>12.2f}")


def add_expense(path, expenses):
    raw = input("Enter amount: ")
    try:
        amount, exact = read_amount(raw)
    except (ValueError, ArithmeticError):
        print("Invalid Data. Please enter a number like 100 or 12.50.")
        return

    if not exact:
        answer = input(f"I read '{raw.strip()}' as {amount:.2f}. Save it? (y/n): ")
        if answer.strip().lower() != "y":
            print("Cancelled.")
            return

    note = input("What was it for? (e.g. food, bus): ").strip() or "-"
    new_id = max((item["id"] for item in expenses), default=0) + 1
    expenses.append({
        "id": new_id,
        "amount": str(amount),
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_expenses(path, expenses)
    print(f"Added {amount:.2f} for '{note}'. Running total: {calculate_total(expenses):.2f}")


def delete_expense(path, expenses):
    if not expenses:
        print("\nNothing to delete.")
        return
    show_expenses(expenses)
    try:
        target = int(input("Enter the ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for item in expenses:
        if item["id"] == target:
            answer = input(f"Delete {Decimal(item['amount']):.2f} ({item['note']})? (y/n): ")
            if answer.strip().lower() == "y":
                expenses.remove(item)
                save_expenses(path, expenses)
                print("Deleted.")
            else:
                print("Cancelled.")
            return
    print("No expense found with that ID.")


def search_expenses(expenses):
    keyword = input("Search by note or amount: ").strip().lower()
    if not keyword:
        print("Please type something to search.")
        return
    results = [
        item for item in expenses
        if keyword in item["note"].lower() or keyword in item["amount"]
    ]
    if results:
        show_expenses(results)
    else:
        print("No matching expenses.")


def main():
    print("=== Expense Tracker ===")
    name = ""
    while not name:
        name = input("What is your name? ").strip()

    path = get_file_path(name)
    expenses = load_expenses(path)

    print(f"\nWelcome, {name}!")
    print("Your expenses are saved here:", path)
    print(f"Current total: {calculate_total(expenses):.2f}")

    while True:
        print("\n1. Add expense")
        print("2. View all expenses")
        print("3. Delete an expense")
        print("4. Search expenses")
        print("5. Show total")
        print("6. Quit")
        choice = input("Choose an option (1-6): ").strip().lower()

        if choice == "1":
            add_expense(path, expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            delete_expense(path, expenses)
        elif choice == "4":
            search_expenses(expenses)
        elif choice == "5":
            print(f"Total Spent: {calculate_total(expenses):.2f}")
        elif choice in ("6", "quit"):
            break
        else:
            print("Invalid option. Please choose 1 to 6.")

    print(f"\nGoodbye, {name}! Total Spent: {calculate_total(expenses):.2f}")


main()