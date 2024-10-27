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
