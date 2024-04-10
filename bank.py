from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

def read_account():
    with open("account.json", "r") as file:
        return json.load(file)

def load_account(data):
    with open("account.json", "w") as file:
        json.dump(data, file)

def today_transactions(account_data, transaction_type):
    today = datetime.now().strftime('%Y-%m-%d')
    return [t for t in account_data['transactions'] if t['date'] == today and t['type'] == transaction_type]


class BankAccountHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', content_type)
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()


    def do_GET(self):
        if self.path == '/balance':
            self.handle_balance()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        if self.path in ['/deposit', '/withdraw']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            self.handle_transaction(json.loads(post_data), self.path.replace('/', ''))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def handle_balance(self):
        self._set_headers()
        account_data = read_account()
        self.wfile.write(json.dumps({'balance': account_data['balance']}).encode())

    def handle_transaction(self, data, transaction_type):
        account_data = read_account()
        amount = data['amount']
        error_message = self.validate_transaction(account_data, transaction_type, amount)
        
        if error_message:
            self._set_headers(400)
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
        self._set_headers()
        self.wfile.write(json.dumps({'message': 'Transaction successful', 'new_balance': account_data['balance']}).encode())

    def validate_transaction(self, account_data, transaction_type, amount):
        if transaction_type == "deposit":
            if amount > 40000: return "Exceeded Maximum Deposit Per Transaction"
            if sum(t['amount'] for t in today_transactions(account_data, "deposit")) + amount > 150000: return "Exceeded Maximum Deposit for the Day"
            if len(today_transactions(account_data, "deposit")) >= 4: return "Exceeded Maximum Deposit Frequency"
        elif transaction_type == "withdraw":
            if amount > 20000: return "Exceeded Maximum Withdrawal Per Transaction"
            if sum(t['amount'] for t in today_transactions(account_data, "withdraw")) + amount > 50000: return "Exceeded Maximum Withdrawal for the Day"
            if len(today_transactions(account_data, "withdraw")) >= 3: return "Exceeded Maximum Withdrawal Frequency"
            if account_data['balance'] < amount: return "Insufficient Balance"
        return ""

def run(server_class=HTTPServer, handler_class=BankAccountHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
