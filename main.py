from decimal import Decimal
from json import dumps

from modules import read_holdings

if __name__ == "__main__":
    todays_date = input("Enter today's date (format: YYYY-MM-DD): ")
    file_path = f"./holdings/holdings-report-{todays_date}.csv"
    todays_deposit = Decimal(input("Enter the amount you're investing today: "))
    print("\n")
    print(dumps(read_holdings(file_path, todays_deposit), default=str, indent=2))
