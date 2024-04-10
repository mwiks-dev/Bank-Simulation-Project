import tkinter as tk
from tkinter import messagebox
import requests

# Adjust the URL to match your server configuration
API_URL = "http://localhost:8000"

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Account Service")
        self.geometry("300x200")

        self.balance_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        tk.Label(self, text="Balance:").pack()
        tk.Label(self, textvariable=self.balance_var).pack()

        tk.Label(self, text="Amount:").pack()
        tk.Entry(self, textvariable=self.amount_var).pack()

        tk.Button(self, text="Deposit", command=self.deposit).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Withdraw", command=self.withdraw).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self, text="Refresh Balance", command=self.get_balance).pack(fill=tk.X, padx=50, pady=5)

        self.get_balance()

    def get_balance(self):
        try:
            response = requests.get(f"{API_URL}/balance")
            if response.status_code == 200:
                balance = response.json()['balance']
                self.balance_var.set(f"$ {balance}")
            else:
                messagebox.showerror("Error", "Failed to fetch balance")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def deposit(self):
        self.transaction("deposit")

    def withdraw(self):
        self.transaction("withdraw")

    def transaction(self, transaction_type):
        amount = self.amount_var.get()
        try:
            response = requests.post(f"{API_URL}/{transaction_type}", json={"amount": float(amount)})
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json().get("message", "Transaction successful"))
                self.get_balance()
            else:
                messagebox.showerror("Error", response.json().get("error", "Transaction failed"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")
        finally:
            self.amount_var.set("")

if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
