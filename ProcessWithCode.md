# Step-by-Step Documentation

### 1. Setting Up the Environment

** Install Python: **
Ensure you have Python installed. You can download it from the official website.

** Install Required Libraries: **
Open your terminal or command prompt and run the following commands to install the necessary libraries:

```bash
pip install flask requests
```

** Tkinter: **
Tkinter is included with standard Python installations. If you're using a version of Python that doesn't include Tkinter, you may need to install it separately. For most users, this won't be necessary.

### 2. Deploying the Blockchain Server

** blockchain.py **

Create a file named blockchain.py with the following content:

```python
import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)  # Genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        self.chain[-1]["current_hash"] = self.hash(self.chain[-1])
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        self.new_block(proof=100, previous_hash=self.chain[-1]["current_hash"])
        return self.last_block['index']

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
```

** blockchain_server.py **

Create another file named blockchain_server.py with the following content:

```python
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
```

** Running the Blockchain Server: **

Open a terminal or command prompt, navigate to the directory containing blockchain_server.py, and run the server:

```bash
python blockchain_server.py
```

### 3. Running the AV Simulator

** av_simulator.py **

Create a file named av_simulator.py with the following content:

```python
import tkinter as tk
from tkinter import scrolledtext, font
import threading
import time
import requests
import random

counter = 1

class AutonomousVehicleSimulator:
    def __init__(self, blockchain_url, text_area, blockchain_app):
        self.blockchain_url = blockchain_url
        self.text_area = text_area
        self.blockchain_app = blockchain_app
        self.running = False

    def send_data_to_blockchain(self, data):
        global counter
        try:
            response = requests.post(self.blockchain_url, json=data)
            if response.status_code == 201:
                self.text_area.insert(tk.END, f"Transaction will be added to Block {counter + 1}\n")
                self.text_area.insert(tk.END, f"{data['sender']}, {data['recipient']}, {data['amount']} \n")
                self.text_area.insert(tk.END, "Data added to blockchain successfully.\n\n")
                counter += 1
            else:
                self.text_area.insert(tk.END, f"Failed to add data to blockchain: {response.text}\n")
        except requests.RequestException as e:
            self.text_area.insert(tk.END, f"Error communicating with blockchain: {e}\n")

    def generate_vehicle_data(self):
        while self.running:
            location = self.generate_location()
            speed = self.generate_speed()
            acceleration = self.generate_acceleration()

            data = {
                'sender': 'Autonomous Vehicle',
                'recipient': 'Blockchain',
                'amount': {
                    'location': location,
                    'speed': speed,
                    'acceleration': acceleration,
                }
            }

            self.send_data_to_blockchain(data)
            time.sleep(10)

    def generate_location(self):
        latitude = round(random.uniform(40.0, 45.0), 4)
        longitude = round(random.uniform(-80.0, -75.0), 4)
        return f"{latitude}° N, {longitude}° W"

    def generate_speed(self):
        return round(random.uniform(0, 100), 2)

    def generate_acceleration(self):
        return round(random.uniform(-5, 5), 2)

class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autonomous Vehicle Data Simulator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.tk_setPalette(background='#212121', foreground='white')

        self.text_area = scrolledtext.ScrolledText(self.root, width=60, height=20, bg='#212121', fg='white',
                                                   selectbackground='#1565C0', selectforeground='white')
        self.text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.text_area.grid_rowconfigure(0, weight=1)
        self.text_area.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.av_simulator = AutonomousVehicleSimulator("http://localhost:5000/add_data", self.text_area, self)

        self.font_size = 10
        self.update_font_size()
        self.root.bind("<Control-plus>", self.increase_font_size)
        self.root.bind("<Control-minus>", self.decrease_font_size)

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation, bg='#424242', fg='white')
        self.start_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.stop_button = tk.Button(self.root, text="Stop Simulation", command=self.stop_simulation, state=tk.DISABLED, bg='#424242', fg='white')
        self.stop_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    def start_simulation(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.av_simulator.running = True
        av_thread = threading.Thread(target=self.av_simulator.generate_vehicle_data)
        av_thread.start()

    def stop_simulation(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.av_simulator.running = False

    def increase_font_size(self, event=None):
        self.font_size += 1
        self.update_font_size()

    def decrease_font_size(self, event=None):
        if self.font_size > 1:
            self.font_size -= 1
            self.update_font_size()

    def update_font_size(self):
        updated_font = font.Font(family="TkDefaultFont", size=self.font_size)
        self.text_area.configure(font=updated_font)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
```

** Running the AV Simulator: **
Open another terminal or command prompt, navigate to the directory containing av_simulator.py, and run the simulator:

```bash
python av_simulator.py
```

### 4. Running the Blockchain Block Visualizer

** block_visualizer.py **

Create a file named block_visualizer.py with the following content:

```python
import tkinter as tk
from tkinter import scrolledtext, font
import requests
import json

class BlockchainVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Block Visualizer")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        self.root.tk_setPalette(background='#212121', foreground='white')

        self.blocks_text = scrolledtext.ScrolledText(self.root, width=60, height=20, bg='#212121', fg='white',
                                                     selectbackground='#1565C0', selectforeground='white')
        self.blocks_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.blocks_text.grid_rowconfigure(0, weight=1)
        self.blocks_text.grid_columnconfigure(0, weight=1)

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_blocks, bg='#424242', fg='white')
        self.refresh_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.blocks_text.bind("<Control-plus>", self.increase_font_size)
        self.blocks_text.bind("<Control-minus>", self.decrease_font_size)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.font_size = 10
        self.update_font_size()

    def increase_font_size(self, event):
        self.font_size += 1
        self.update_font_size()

    def decrease_font_size(self, event):
        if (self.font_size > 1):
            self.font_size -= 1
            self.update_font_size()

    def update_font_size(self):
        updated_font = font.Font(family="TkDefaultFont", size=self.font_size)
        self.blocks_text.configure(font=updated_font)

    def refresh_blocks(self):
        try:
            response = requests.get("http://localhost:5000/chain")
            if response.status_code == 200:
                chain = response.json()["chain"]
                self.blocks_text.delete(1.0, tk.END)
                for block in chain:
                    self.blocks_text.insert(tk.END, f"Block Index: {block['index']}\n")
                    self.blocks_text.insert(tk.END, f"Current Hash: {block['current_hash']}\n")
                    self.blocks_text.insert(tk.END, f"Timestamp: {block['timestamp']}\n")
                    self.blocks_text.insert(tk.END, f"Transactions: {json.dumps(block['transactions'])}\n")
                    self.blocks_text.insert(tk.END, f"Proof: {block['proof']}\n")
                    self.blocks_text.insert(tk.END, f"Previous Hash: {block['previous_hash']}\n\n")
            else:
                self.blocks_text.insert(tk.END, f"Failed to retrieve blockchain data: {response.text}\n")
        except requests.RequestException as e:
            self.blocks_text.insert(tk.END, f"Error communicating with blockchain: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainVisualizerApp(root)
    root.mainloop()
```

** Running the Blockchain Block Visualizer: **

Open another terminal or command prompt, navigate to the directory containing block_visualizer.py, and run the visualizer:

```bash
python block_visualizer.py
```



