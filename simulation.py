from blockchain.blockchain import Blockchain
from blockchain.node import Node
from blockchain.transaction import Transaction
from wallet.wallet import Wallet

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

    # Crear una transacción
    transaction = Transaction(wallet1.public_key, wallet2.public_key, 10).to_dict()
    node1.receive_transaction(transaction)

    # Validar si todos los nodos coinciden antes de minar el bloque
    if node1.validate_all_nodes():
        mined_block = node1.mine_block()
        # Recompensa por minar un bloque válido
        wallet1.add_balance(2)
    else:
        print("Error: Los nodos no coinciden, no se puede minar el bloque.")

    # Mostrar el estado de la blockchain
    print("Blockchain:")
    for block in blockchain.chain:
        print(block)

    # Verificar la validez de la blockchain
    print("Blockchain válida:", blockchain.is_valid_chain(blockchain.chain))

if __name__ == "__main__":
    simulate_blockchain()