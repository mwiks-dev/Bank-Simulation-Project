import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

def account_info():
    with open("account.json", "r") as file:
        return json.load(file)
    
def load_account(data):
    with open("account.json", "w") as file:
        json.dump(data, file)

def validate_transaction(transaction_type, amount, account_data):
    max_deposit_per_day = 150000
    max_deposit_per_transaction = 40000
    max_withdrawal_per_day = 50000
    max_withdrawal_per_transaction = 20000
    daily_transactions = sum(t['amount'] for t in account_data['transactions'] if t['date'] == datetime.now().strftime('%Y-%m-%d') and t['type'] == transaction_type)

    if transaction_type == "deposit":
        if amount > max_deposit_per_transaction:
            return "Exceeded Maximum Deposit Per Transaction", 403
        elif daily_transactions + amount > max_deposit_per_day:
            return "Exceeded Maximum Deposit for the Day", 403
        elif len([t for t in account_data['transactions'] if t['date'] == datetime.now().strftime('%Y-%m-%d') and t['type'] == 'deposit']) >= 4:
            return "Exceeded Maximum Deposit Frequency", 403
    elif transaction_type == "withdraw":
        if amount > max_withdrawal_per_transaction:
            return "Exceeded Maximum Withdrawal Per Transaction", 403
        elif daily_transactions + amount > max_withdrawal_per_day:
            return "Exceeded Maximum Withdrawal for the Day", 403
        elif len([t for t in account_data['transactions'] if t['date'] == datetime.now().strftime('%Y-%m-%d') and t['type'] == 'withdraw']) >= 3:
            return "Exceeded Maximum Withdrawal Frequency", 403
        elif account_data['balance'] < amount:
            return "Insufficient Balance", 403
    return None, 200

