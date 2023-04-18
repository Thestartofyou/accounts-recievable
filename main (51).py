import csv
import datetime

class Account:
    def __init__(self, name, balance, last_payment_date):
        self.name = name
        self.balance = balance
        self.last_payment_date = last_payment_date
    
    def add_transaction(self, amount):
        self.balance += amount
    
    def update_last_payment_date(self, date):
        self.last_payment_date = date
    
    def is_overdue(self, days):
        today = datetime.date.today()
        payment_due_date = self.last_payment_date + datetime.timedelta(days=days)
        return today > payment_due_date
    
    def __str__(self):
        overdue_days = (datetime.date.today() - (self.last_payment_date + datetime.timedelta(days=30))).days
        overdue_text = f" (overdue by {overdue_days} days)" if self.is_overdue(30) else ""
        return f"{self.name}: {self.balance}{overdue_text}"
    
class AccountsReceivable:
    def __init__(self):
        self.accounts = []
    
    def add_account(self, account):
        self.accounts.append(account)
    
    def get_account(self, name):
        for account in self.accounts:
            if account.name == name:
                return account
        return None
    
    def add_transaction(self, name, amount):
        account = self.get_account(name)
        if account is None:
            account = Account(name, 0, datetime.date.today())
            self.add_account(account)
        account.add_transaction(amount)
        account.update_last_payment_date(datetime.date.today())
    
    def generate_report(self):
        for account in self.accounts:
            if account.is_overdue(30):
                print(f"Reminder: Payment for {account.name} is overdue by {(datetime.date.today() - (account.last_payment_date + datetime.timedelta(days=30))).days} days.")
            print(account)

ar = AccountsReceivable()

# Read transactions from CSV file
with open('transactions.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader) # skip header row
    for row in reader:
        name, amount = row
        ar.add_transaction(name, float(amount))

ar.generate_report()
