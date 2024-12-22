class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        import hashlib
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

    @classmethod
    def from_dict(cls, block_dict):
        return cls(
            block_dict['index'],
            block_dict['timestamp'],
            block_dict['transactions'],
            block_dict['previous_hash']
        )