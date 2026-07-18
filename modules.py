from dotenv import load_dotenv
from decimal import Decimal
from csv import reader
from os import getenv

load_dotenv()



TARGET_WEIGHTS = {
    getenv("STOCK_1"): Decimal("0.1"),
    getenv("STOCK_2"): Decimal("0.3"),
    getenv("STOCK_3"): Decimal("0.57"),
    getenv("STOCK_4"): Decimal("0.03")
}

def is_drifted(portfolio, total_invested):
    """
    Determines whether significant drift is detected to assist main calculations in corrections.

    Note: This is no longer being used as it's only beneficial in cases where you need to consider
    capital gains, taxes, investment fees, etc... I've instead opted to just use target weights in each
    investment which keeps my portfolio aligned within a small margin of error.
    """
    
    DRIFT_THRESHOLD_UPPER_BOUND = Decimal("0.02")
    drift = False
    for stock in portfolio:
        current_weight = portfolio[stock]["amount_invested"] / total_invested
        drift_amount = current_weight - TARGET_WEIGHTS[stock]
        portfolio[stock]["drift_amount"] = Decimal(str(drift_amount))
        abs_drift_amount = abs(drift_amount)
        if abs_drift_amount >= DRIFT_THRESHOLD_UPPER_BOUND:
            drift = True
    return drift

def read_holdings(file_path, deposit):
    portfolio = {}
    total_invested = 0
    with open(file_path, "r") as file:
        read_file = reader(file)
        next(read_file)
        for line in read_file:
            # Reader includes a few extra lines that would break the code below the if-statement
            if len(line) == 0: break
            weight = TARGET_WEIGHTS[line[4]]
            portfolio[line[4]] = {
                "share_price": Decimal(line[11]),
                "amount_invested": Decimal(line[17]),
                "amount_to_invest": round(Decimal(weight * deposit), 2)
            }
            total_invested += portfolio[line[4]]["amount_invested"]
    return portfolio
