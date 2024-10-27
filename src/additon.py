# src/bank.py

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class BankAccount:
    def __init__(self, account_holder, balance=0.0):
        """Initialize an account with an account holder name and an optional balance."""
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        """Deposit a specific amount to the account balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Withdraw a specific amount from the account balance."""
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds in the account.")
        self.balance -= amount
        return self.balance

    def transfer(self, amount, other_account):
        """Transfer a specific amount from this account to another account."""
        self.withdraw(amount)  # This may raise InsufficientFundsError
        other_account.deposit(amount)
        return self.balance, other_account.balance

# src/tests/test_bank.py
import pytest
from bank import BankAccount, InsufficientFundsError

def test_account_creation():
    """Test creating an account with an initial balance."""
    account = BankAccount("Alice", 100)
    assert account.balance == 100
    assert account.account_holder == "Alice"

def test_deposit():
    """Test depositing money to the account."""
    account = BankAccount("Bob", 50)
    new_balance = account.deposit(50)
    assert new_balance == 100

def test_withdraw():
    """Test withdrawing money from the account."""
    account = BankAccount("Charlie", 100)
    new_balance = account.withdraw(40)
    assert new_balance == 60

def test_withdraw_insufficient_funds():
    """Test withdrawing more money than available in the account."""
    account = BankAccount("David", 20)
    with pytest.raises(InsufficientFundsError, match="Insufficient funds"):
        account.withdraw(50)

def test_deposit_negative_amount():
    """Test depositing a negative amount, expecting ValueError."""
    account = BankAccount("Eve", 0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-10)

def test_withdraw_negative_amount():
    """Test withdrawing a negative amount, expecting ValueError."""
    account = BankAccount("Frank", 100)
    with pytest.raises(ValueError, match="Withdraw amount must be positive"):
        account.withdraw(-30)

def test_transfer_funds():
    """Test transferring funds between two accounts."""
    account1 = BankAccount("Alice", 100)
    account2 = BankAccount("Bob", 50)
    account1.transfer(40, account2)
    assert account1.balance == 60
    assert account2.balance == 90

def test_transfer_insufficient_funds():
    """Test transferring funds with insufficient balance, expecting InsufficientFundsError."""
    account1 = BankAccount("Alice", 30)
    account2 = BankAccount("Bob", 100)
    with pytest.raises(InsufficientFundsError, match="Insufficient funds"):
        account1.transfer(50, account2)
