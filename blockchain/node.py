import requests
from blockchain.block import Block
import time

class Node:
    def __init__(self, node_id, blockchain):
        self.node_id = node_id
        self.blockchain = blockchain
        self.peers = set()

    def connect_to_peer(self, peer_node):
        self.peers.add(peer_node)

    def wait_for_peers(self):
        for peer in self.peers:
            connected = False
            while not connected:
                try:
                    response = requests.get(f"{peer}/ping")
                    if response.status_code == 200:
                        connected = True
                except requests.exceptions.ConnectionError:
                    print(f"Esperando a que {peer} esté disponible...")
                    time.sleep(2)
                except Exception as e:
                    print(f"Error inesperado al conectar con {peer}: {e}")
                    time.sleep(2)

    def sync_blockchain(self):
        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/blockchain")
                if response.status_code == 200:
                    peer_blockchain = response.json()
                    self.blockchain.replace_chain(peer_blockchain)
            except requests.exceptions.ConnectionError:
                print(f"Error: No se pudo conectar a {peer}")
            except Exception as e:
                print(f"Error inesperado al sincronizar con {peer}: {e}")

    def broadcast_new_block(self, block):
        block_obj = Block.from_dict(block)
        for peer in self.peers:
            try:
                requests.post(f"{peer}/block", json=block_obj.to_dict())
            except requests.exceptions.ConnectionError:
                print(f"Error: No se pudo conectar a {peer}")
            except Exception as e:
                print(f"Error inesperado al transmitir a {peer}: {e}")

        # Enviar el nuevo bloque al dashboard
        try:
            requests.post('http://localhost:5500/dashboard/update', json=block_obj.to_dict())
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar al dashboard")
        except Exception as e:
            print(f"Error inesperado al transmitir al dashboard: {e}")

    def receive_new_block(self, block):
        # Convertir el bloque recibido a un objeto de bloque
        new_block = Block(
            block['index'],
            block['timestamp'],
            block['transactions'],
            block['previous_hash']
        )
        # Verificar si el nuevo bloque es válido y agregarlo a la cadena
        if self.blockchain.is_valid_new_block(new_block):
            self.blockchain.add_block(new_block)

    def get_peers(self):
        return list(self.peers)

    def receive_transaction(self, transaction):
        self.blockchain.add_transaction(
            transaction['sender'],
            transaction['recipient'],
            transaction['amount']
        )

    def mine_block(self):
        last_block = self.blockchain.last_block
        last_proof = last_block['proof']
        proof = self.blockchain.proof_of_work(last_proof)
        previous_hash = last_block['hash']
        
        # Obtener las primeras 3 transacciones
        transactions = self.blockchain.current_transactions[:3]
        
        # Crear el bloque con las 3 transacciones
        block = self.blockchain.create_block(proof, previous_hash, transactions)
        
        # Eliminar las transacciones minadas de la lista de transacciones actuales
        self.blockchain.current_transactions = self.blockchain.current_transactions[3:]
        
        self.broadcast_new_block(block)
        return block

    def validate_all_nodes(self):
        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/chain")
                if response.status_code == 200:
                    peer_chain = response.json()['chain']
                    if not self.blockchain.is_valid_chain(peer_chain):
                        return False
            except requests.exceptions.ConnectionError:
                print(f"Error: No se pudo conectar a {peer}")
                return False
        return True