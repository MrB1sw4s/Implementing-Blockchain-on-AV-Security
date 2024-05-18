from flask import Flask, request, jsonify
from blockchain import Blockchain

app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    index = blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
