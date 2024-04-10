import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

def account_info():
    with open("account.json", "r") as file:
        return json.load(file)
    
def load_account(data):
    with open("account.json", "w") as file:
        json.dump(data, file)

