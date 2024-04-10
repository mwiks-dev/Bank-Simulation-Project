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

class BankAccount(BaseHTTPRequestHandler):
    def set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def get_data(self):
        if self.path == '/balance':
            self.balance()
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def post_data(self):
        if self.path in ['/deposit', '/withdraw']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.transaction(post_data, self.path.replace('/', ''))
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def balance(self):
        self.set_headers(200)
        account_data = account_info()
        self.wfile.write(json.dumps({'balance': account_data['balance']}).encode())

    def transaction(self, post_data, transaction_type):
        try:
            data = json.loads(post_data)
            amount = data.get('amount')
            if amount is None:
                raise ValueError("Amount is required")

            account_data = account_info()
            error_message, status_code = validate_transaction(transaction_type, amount, account_data)
            if status_code != 200:
                self.set_headers(status_code)
                self.wfile.write(json.dumps({'error': error_message}).encode())
                return

            if transaction_type == "deposit":
                account_data['balance'] += amount
            elif transaction_type == "withdraw":
                account_data['balance'] -= amount

            account_data['transactions'].append({
                "type": transaction_type,
                "amount": amount,
                "date": datetime.now().strftime('%Y-%m-%d')
            })

            load_account(account_data)
            self.set_headers(200)
            self.wfile.write(json.dumps({"message": "Transaction successful", "balance": account_data['balance']}).encode())

        except ValueError as e:
            self.set_headers(400)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

def run(server_class=HTTPServer, handler_class=BankAccount, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
