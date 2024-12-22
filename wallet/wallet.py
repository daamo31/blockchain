from wallet.keys import Keys
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self):
        self.balance = 0
        self.transactions = []
        self.keys = Keys()
        self.private_key, self.public_key = self.keys.generate_key_pair()

    def create_transaction(self, recipient, amount):
        if amount > self.balance:
            raise ValueError("Saldo insuficiente para realizar la transacción.")
        transaction = {
            'sender': self.get_public_key(),
            'recipient': recipient,
            'amount': amount
        }
        self.transactions.append(transaction)
        self.balance -= amount
        return transaction

    def get_balance(self):
        return self.balance

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    def add_balance(self, amount):
        self.balance += amount

    def get_transactions(self):
        return self.transactions