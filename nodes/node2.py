import sys
import os

import requests
from flask import Flask
from threading import Thread
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blockchain.blockchain import Blockchain
from blockchain.node import Node
from blockchain.transaction import Transaction
from wallet.wallet import Wallet

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

def start_server():
    app.run(host='0.0.0.0', port=5052)

def main():
    # Inicializar la cadena de bloques
    blockchain = Blockchain()
    
    # Crear un nodo
    node = Node(node_id=2, blockchain=blockchain)
    
    # Crear una billetera
    wallet = Wallet()
    
    # Conectar con otros nodos (por ejemplo, node1 y node3)
    node.connect_to_peer("http://localhost:5051")  # Conectar a node1
    node.connect_to_peer("http://localhost:5053")  # Conectar a node3
    
    # Esperar a que los otros nodos estén disponibles
    node.wait_for_peers()
    
    # Comenzar la sincronización
    try:
        node.sync_blockchain()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a uno de los nodos.")

    # Recibir transacciones y minar bloques
    transaction = Transaction('sender', 'recipient', 10).to_dict()
    node.receive_transaction(transaction)
    mined_block = node.mine_block()

    # Recompensa por minar un bloque válido
    wallet.add_balance(2)

if __name__ == "__main__":
    server_thread = Thread(target=start_server)
    server_thread.start()
    main()