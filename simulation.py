# filepath: /Users/daniel/Desktop/blockchain/basic-blockchain/simulation.py
from blockchain.blockchain import Blockchain
from blockchain.node import Node
from blockchain.transaction import Transaction
from wallet.wallet import Wallet
import time

def simulate_blockchain():
    # Crear una instancia de la blockchain
    blockchain = Blockchain()

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

    # Función para crear y enviar una transacción
    def create_and_send_transaction(sender_wallet, recipient_wallet, amount):
        transaction = Transaction(sender_wallet.public_key, recipient_wallet.public_key, amount).to_dict()
        node1.receive_transaction(transaction)

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
            print(block.__dict__)  # Convertir objeto a diccionario

        # Verificar la validez de la blockchain
        print("Blockchain válida:", blockchain.is_valid_chain(blockchain.chain))

        # Esperar un tiempo antes de intentar minar el siguiente bloque
        time.sleep(10)  # Esperar 10 segundos

if __name__ == "__main__":
    simulate_blockchain()