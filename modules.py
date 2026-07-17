from dotenv import load_dotenv
from decimal import Decimal
from csv import reader
from os import getenv

load_dotenv()


DRIFT_THRESHOLD = Decimal("0.05")

TARGET_WEIGHTS = {
    getenv("STOCK_1"): Decimal("0.1"),
    getenv("STOCK_2"): Decimal("0.3"),
    getenv("STOCK_3"): Decimal("0.57"),
    getenv("STOCK_4"): Decimal("0.03")
}

def is_drifted(portfolio, total_invested):
    for stock in portfolio:
        current_weight = portfolio[stock]["amount_invested"] / total_invested
        drift_amount = abs(current_weight - TARGET_WEIGHTS[stock])
        if drift_amount >= DRIFT_THRESHOLD:
            return True
    return False

def read_holdings(file_path, deposit):
    portfolio = {}
    total_invested = 0
    with open(file_path, "r") as file:
        read_file = reader(file)
        next(read_file)
        for line in read_file:
            if len(line) == 0: break
            portfolio[line[4]] = {
                "share_price": Decimal(line[11]),
                "amount_invested": Decimal(line[17])
            }
            total_invested += portfolio[line[4]]["amount_invested"]
        drifted = is_drifted(portfolio, total_invested)
        for stock in portfolio:
            if drifted:
                weight = TARGET_WEIGHTS[stock]
            else:
                weight = portfolio[stock]["amount_invested"] / total_invested
            portfolio[stock]["amount_to_invest"] = round(Decimal(weight * deposit), 2)
    return portfolio
