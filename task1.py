
from abc import ABC, abstractmethod


# ABSTRACT BASE CLASS

class Account(ABC):

    def __init__(self, account_number, owner, initial_balance=0.0, currency="MAD"):

        self.__account_number = account_number
        self.__owner = owner
        self.__balance = float(initial_balance)
        self.__currency = currency

    @property
    def account_number(self):
        return self.__account_number

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    @property
    def currency(self):
        return self.__currency

    def deposit(self, amount):

        if amount <= 0 or amount != amount or amount == float("inf") or amount == float("-inf"):
            raise ValueError("Deposit amount must be positive and finite")

        self.__balance += amount

    def withdraw(self, amount):

        if amount <= 0 or amount != amount or amount == float("inf") or amount == float("-inf"):
            raise ValueError("Withdrawal amount must be positive and finite")

        if amount > self.__balance:
            raise ValueError("Insufficient funds")

        self.__balance -= amount

    @abstractmethod
    def accrue_interest(self):
        pass

    @abstractmethod
    def deduct_fee(self):
        pass


# SAVINGS ACCOUNT

class SavingsAccount(Account):

    def accrue_interest(self):

        interest = self.balance * 0.02
        self.deposit(interest)

    def deduct_fee(self):
        return


# CHECKING ACCOUNT

class CheckingAccount(Account):

    def accrue_interest(self):
        return

    def deduct_fee(self):

        self.withdraw(10.0)


# HIGH YIELD ACCOUNT

class HighYieldAccount(Account):

    def accrue_interest(self):

        interest = self.balance * 0.05
        self.deposit(interest)

    def deduct_fee(self):

        self.withdraw(5.0)


# BANK LEDGER

class BankLedger:

    def __init__(self):

        self.__accounts = []
        self.__transactions = []

    def add_account(self, account):

        for acc in self.__accounts:

            if acc.account_number == account.account_number:
                raise ValueError("Account already exists")

        self.__accounts.append(account)

    def get_account(self, account_number):

        for acc in self.__accounts:

            if acc.account_number == account_number:
                return acc

        raise ValueError("Account not found")

    def transfer(self, sender_number, receiver_number, amount):

        sender = self.get_account(sender_number)
        receiver = self.get_account(receiver_number)

        if sender.account_number == receiver.account_number:
            raise ValueError("Cannot transfer to the same account")

        if sender.currency != receiver.currency:
            raise ValueError("Cannot transfer between different currencies")

        sender.withdraw(amount)
        receiver.deposit(amount)

        self.__transactions.append(
            f"Transfer: {amount} {sender.currency} "
            f"from {sender_number} to {receiver_number}"
        )

    def process_monthly_updates(self):

        for acc in self.__accounts:

            acc.accrue_interest()
            acc.deduct_fee()

    def show_accounts(self):

        for acc in self.__accounts:

            print("-----------------------------")
            print("Account:", acc.account_number)
            print("Owner:", acc.owner)
            print("Balance:", acc.balance, acc.currency)
            print("Type:", type(acc).__name__)

    def show_transactions(self):

        for transaction in self.__transactions:
            print(transaction)


# TESTING THE SYSTEM


ledger = BankLedger()

savings = SavingsAccount(1001, "Ayman", 1000, "MAD")
checking = CheckingAccount(1002, "mohammed", 2000, "MAD")
high_yield = HighYieldAccount(1003, "saad", 3000, "USD")

ledger.add_account(savings)
ledger.add_account(checking)
ledger.add_account(high_yield)

savings.deposit(500)
checking.withdraw(200)

ledger.transfer(1001, 1002, 100)

ledger.process_monthly_updates()

ledger.show_accounts()

print("\n transaction history")
ledger.show_transactions()
