import unittest
import json
from http.client import HTTPConnection

class TestBankAccountService(unittest.TestCase):
    def setUp(self):
        self.conn = HTTPConnection("localhost", 8000)
    
    def test_balance(self):
        self.conn.request("GET", "/balance")
        response = self.conn.getresponse()
        data = json.loads(response.read().decode())
        self.assertEqual(response.status, 200)
        self.assertTrue('balance' in data)
    
    def test_deposit(self):
        # Perform a deposit
        deposit_amount = {"amount": 100}
        self.conn.request("POST", "/deposit", body=json.dumps(deposit_amount), headers={"Content-Type": "application/json"})
        deposit_response = self.conn.getresponse()
        self.assertEqual(deposit_response.status, 200)
        deposit_data = json.loads(deposit_response.read().decode())
        self.assertIn('message', deposit_data)
        
        # Check balance after deposit
        self.conn.request("GET", "/balance")
        balance_response = self.conn.getresponse()
        balance_data = json.loads(balance_response.read().decode())
        self.assertEqual(balance_response.status, 200)
        self.assertTrue(balance_data['balance'] >= 100)  # Assuming initial balance is 0 or more
    
    def test_withdraw(self):
        # Assuming there's enough balance from previous tests or initial setup
        withdraw_amount = {"amount": 50}
        self.conn.request("POST", "/withdraw", body=json.dumps(withdraw_amount), headers={"Content-Type": "application/json"})
        withdraw_response = self.conn.getresponse()
        self.assertEqual(withdraw_response.status, 200)
        withdraw_data = json.loads(withdraw_response.read().decode())
        self.assertIn('message', withdraw_data)
        
        # Check balance after withdrawal
        self.conn.request("GET", "/balance")
        balance_response = self.conn.getresponse()
        balance_data = json.loads(balance_response.read().decode())
        self.assertEqual(balance_response.status, 200)
        self.assertTrue(balance_data['balance'] >= 50)  # Adjust according to initial balance and deposit
    
    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
