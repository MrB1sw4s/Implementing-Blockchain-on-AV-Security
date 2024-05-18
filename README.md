# Autonomous Vehicle Data Simulation with Blockchain Integration

## Project Overview

This project simulates an autonomous vehicle (AV) that generates random data and sends it to a blockchain server. The blockchain server records this data in blocks, and a visualizer displays the current state of the blockchain.

## Project Structure

1. **Blockchain Server** (`blockchain_server.py` and `blockchain.py`): 
   - Receives data from the AV simulator and stores it in the blockchain.

2. **AV Simulator** (`av_simulator.py`):
   - Generates random AV data such as location, speed, and acceleration.
   - Sends this data to the blockchain server at regular intervals.

3. **Block Visualizer** (`block_visualizer.py`):
   - Retrieves the blockchain data from the server and displays it in a user-friendly interface.

## Setup Instructions

### Prerequisites

- Python 3.x
- Required Python libraries: Flask, Requests, Tkinter

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository-url.git  ///////
   cd your-repository-directory

2. **Install Required Libraries:**
   ```bash
   pip install flask requests
   ```

### Running the Project

#### Start the Blockchain Server:
1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the blockchain server:
   ```bash
   python blockchain_server.py
   ```

#### Start the AV Simulator:
1. Open another terminal or command prompt.
2. Navigate to the project directory.
3. Run the AV simulator:
   ```bash
   python av_simulator.py
   ```

#### Start the Blockchain Block Visualizer:
1. Open another terminal or command prompt.
2. Navigate to the project directory.
3. Run the block visualizer:
   ```bash
   python block_visualizer.py
   ```

### Usage
- The AV simulator will generate random data and send it to the blockchain server every 10 seconds.
- The blockchain server will store the data in blocks.
- The block visualizer will display the current state of the blockchain, including block details such as index, current hash, timestamp, transactions, proof, and previous hash.

### Project Files
- `blockchain.py`: Defines the Blockchain class and methods for creating blocks and transactions.
- `blockchain_server.py`: Flask application that serves as the blockchain server.
- `av_simulator.py`: Tkinter-based application simulating an AV and sending data to the blockchain server.
- `block_visualizer.py`: Tkinter-based application visualizing the blockchain data.
