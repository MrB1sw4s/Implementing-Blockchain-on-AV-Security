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
