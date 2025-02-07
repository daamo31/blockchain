from blockchain.blockchain import Blockchain
from blockchain.node import Node
from blockchain.transaction import Transaction
from wallet.wallet import Wallet
import time
import requests
from cryptography.hazmat.primitives import serialization

# Crear una instancia de la blockchain
blockchain = Blockchain()

def simulate_blockchain():
    # Crear billeteras y nodos
    wallet1 = Wallet()
    wallet2 = Wallet()
    node1 = Node(node_id=1, blockchain=blockchain)
    node2 = Node(node_id=2, blockchain=blockchain)
    node3 = Node(node_id=3, blockchain=blockchain)

    # Conectar nodos entre sí
    node1.connect_to_peer("http://localhost:5052")
    node1.connect_to_peer("http://localhost:5053")
    node2.connect_to_peer("http://localhost:5051")
    node2.connect_to_peer("http://localhost:5053")
    node3.connect_to_peer("http://localhost:5051")
    node3.connect_to_peer("http://localhost:5052")

    # Función para crear y enviar una transacción a través de la API
    def create_and_send_transaction(sender_wallet, recipient_wallet, amount):
        if sender_wallet.balance < amount:
            print("Error: Saldo insuficiente para realizar la transacción.")
            return

        transaction_data = {
            'sender': sender_wallet.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8'),
            'recipient': recipient_wallet.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8'),
            'amount': amount
        }
        response = requests.post('http://localhost:5500/wallet/transaction', json=transaction_data)
        if response.status_code == 201:
            print("Transacción creada y enviada con éxito.")
        else:
            print(f"Error al enviar la transacción: {response.text}")

    # Bucle para la minería automática de bloques
    while True:
        # Crear una transacción
        create_and_send_transaction(wallet1, wallet2, 10)

        # Validar si todos los nodos coinciden antes de minar el bloque
        if node1.validate_all_nodes():
            mined_block = node1.mine_block()
            # Recompensa por minar un bloque válido
            wallet1.add_balance(2)
            print(f"Nuevo bloque minado: {mined_block}")
        else:
            print("Error: Los nodos no coinciden, no se puede minar el bloque.")

        # Mostrar el estado de la blockchain
        print("Blockchain:")
        for block in blockchain.chain:
            print(block)  # Asumimos que block ya es un diccionario

        # Verificar la validez de la blockchain
        print("Blockchain válida:", blockchain.is_valid_chain(blockchain.chain))

        # Esperar un tiempo antes de intentar minar el siguiente bloque
        time.sleep(10)  # Esperar 10 segundos

if __name__ == "__main__":
    simulate_blockchain()