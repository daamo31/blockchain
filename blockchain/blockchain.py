from blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': self.get_timestamp(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
            'hash': self.hash_block(len(self.chain) + 1, self.get_timestamp(), self.current_transactions, proof, previous_hash)
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash_block(self, index, timestamp, transactions, proof, previous_hash):
        import hashlib
        block_string = f"{index}{timestamp}{transactions}{proof}{previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_timestamp(self):
        from time import time
        return time()

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        import hashlib
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def is_valid_chain(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            if not self.valid_proof(previous_block['proof'], current_block['proof']):
                return False
        return True

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_valid_chain(new_chain):
            self.chain = [Block.from_dict(block) for block in new_chain]
            return True
        return False