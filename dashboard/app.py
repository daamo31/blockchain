import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from blockchain.blockchain import Blockchain
from blockchain.node import Node
from wallet.wallet import Wallet

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet() 
node = Node(node_id=1, blockchain=blockchain)

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/wallet/balance', methods=['GET'])
def get_balance():
    response = {
        'balance': wallet.get_balance()
    }
    return jsonify(response), 200

@app.route('/wallet/transactions', methods=['GET'])
def get_transactions():
    response = {
        'transactions': wallet.get_transactions()
    }
    return jsonify(response), 200

@app.route('/wallet/transaction', methods=['POST'])
def create_transaction():
    values = request.get_json()
    required = ['recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    transaction = wallet.create_transaction(values['recipient'], values['amount'])
    blockchain.add_transaction(transaction['sender'], transaction['recipient'], transaction['amount'])
    blockchain.broadcast_transaction(transaction)
    response = {'message': 'Transaction will be added to Block and broadcasted to peers'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine_block():
    try:
        block = node.mine_block()
        response = {
            'message': 'New Block Forged',
            'block': block.to_dict()
        }
        return jsonify(response), 200
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'No se pudo conectar a uno de los nodos.'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {e}'}), 500

@app.route('/connect_node', methods=['POST'])
def connect_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "No node", 400
    for node_url in nodes:
        node.connect_to_peer(node_url)
    response = {
        'message': 'All nodes are now connected.',
        'total_nodes': list(node.peers)
    }
    return jsonify(response), 201

if __name__ == '__main__':
    # Conectar nodos entre sí al iniciar la aplicación
    node.connect_to_peer("http://localhost:5051")
    node.connect_to_peer("http://localhost:5052")
    node.connect_to_peer("http://localhost:5053")
    app.run(host='0.0.0.0', port=5500, debug=True)